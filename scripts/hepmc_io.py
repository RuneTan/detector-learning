"""Pythia -> HepMC3 I/O only. No generation loop or detector simulation.

Uses pyhepmc's HEPEVT interface. Explicit vertices avoid the compact-vertex
counting incompatibility of Delphes 3.5.1 with this Pythia event record.
"""
import numpy as np
import pyhepmc


def to_hepmc(pythia, number):
    particles = list(pythia.event)[1:]  # index 0 is Pythia's bookkeeping system
    values = lambda name: np.array([getattr(p, name)() for p in particles])
    event = pyhepmc.GenEvent(pyhepmc.Units.GEV, pyhepmc.Units.MM)
    event.from_hepevt(
        number, values("px"), values("py"), values("pz"), values("e"),
        values("m"), values("id"), values("statusHepMC"),
        parents=np.array([[p.mother1(), p.mother2()] for p in particles]),
        vx=values("xProd"), vy=values("yProd"),
        vz=values("zProd"), vt=values("tProd"),
    )
    for vertex in list(event.vertices):
        if not vertex.particles_out:
            for particle in list(vertex.particles_in):
                vertex.remove_particle_in(particle)
            event.remove_vertex(vertex)
    for vertex in list(event.vertices):
        if not vertex.particles_in:
            for particle in list(vertex.particles_out):
                vertex.remove_particle_out(particle)
            event.remove_vertex(vertex)
        else:
            vertex.status = 1  # force explicit ASCII vertex, not a physics cut
    original = [p for p in particles if p.isFinal()]
    stored = [p for p in event.particles if p.status == 1]
    before = [sum(getattr(p, name)() for p in original) for name in ("px", "py", "pz", "e")]
    after = [sum(getattr(p.momentum, name) for p in stored) for name in ("px", "py", "pz", "e")]
    assert len(stored) == len(original), "Stable particles lost during conversion"
    assert np.allclose(before, after, rtol=0, atol=1e-8), "Four-momentum changed during conversion"
    info = pythia.infoPython()
    event.weights = [info.weight()]
    event.attributes["signal_process_id"] = int(info.code())
    event.attributes["mpi"] = int(info.nMPI())
    event.attributes["event_scale"] = float(info.QRen())
    event.attributes["alphaQCD"] = float(info.alphaS())
    event.attributes["alphaQED"] = float(info.alphaEM())
    cross_section = pyhepmc.GenCrossSection()
    cross_section.set_cross_section(info.sigmaGen() * 1e9, info.sigmaErr() * 1e9)
    event.cross_section = cross_section
    return event
