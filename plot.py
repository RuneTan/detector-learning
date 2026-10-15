#!/usr/bin/env python3
"""Compare existing Delphes and Parnassus outputs with PyROOT; run from project root."""

import argparse
import json
import os
from pathlib import Path


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delphes", type=Path, default=Path("out/delphes.root"))
    parser.add_argument("--parnassus", type=Path, default=Path("out/parnassus.root"))
    parser.add_argument("--out", type=Path, default=Path("out/plots"))
    parser.add_argument("--expect", type=int, default=200,
                        help="expected input events in each tree (default: 200)")
    args = parser.parse_args()
    if args.expect < 1:
        parser.error("--expect must be a positive event count")
    return args


def open_tree(ROOT, path, name, branches):
    if not path.is_file():
        raise RuntimeError(f"Input does not exist: {path}")
    handle = ROOT.TFile.Open(str(path))
    if not handle or handle.IsZombie():
        raise RuntimeError(f"Cannot open ROOT input: {path}")
    tree = handle.Get(name)
    if not tree or not tree.InheritsFrom("TTree"):
        raise RuntimeError(f"Missing TTree {name!r} in {path}")
    missing = [branch for branch in branches if not tree.GetBranch(branch)]
    if missing:
        raise RuntimeError(f"Missing branches in {path}: {', '.join(missing)}")
    return handle, tree


def fill_histograms(ROOT, dt, pt):
    # Count individual muons for pT; one event can contribute several objects.
    ROOT.gROOT.cd()
    title = ";Muon p_{T} [GeV];Normalised entries / bin"
    ht = ROOT.TH1D("htruth", title, 40, 0, 100)
    hd = ROOT.TH1D("hdelphes", title, 40, 0, 100)
    hp = ROOT.TH1D("hparna", title, 40, 0, 100)
    mass_title = ";Leading-pair m_{#mu#mu} [GeV];Normalised entries / bin"
    md = ROOT.TH1D("dimuon_delphes", mass_title, 40, 50, 130)
    mp = ROOT.TH1D("dimuon_parna", mass_title, 40, 50, 130)
    histograms = [ht, hd, hp, md, mp]
    for hist in histograms:
        hist.Sumw2()

    # Delphes already applies isolation; apply the Parnassus selection here.
    draws = [
        (dt, "Particle.PT>>htruth",
         "Particle.Status==1 && abs(Particle.PID)==13 && Particle.PT>10 && abs(Particle.Eta)<2.4"),
        (dt, "Muon.PT>>hdelphes", "Muon.PT>10 && abs(Muon.Eta)<2.4"),
        (pt, "Muons.PT>>hparna",
         "Muons.PT>10 && abs(Muons.Eta)<2.4 && Muons.IsolationVar<0.25"),
    ]
    for tree, expression, selection in draws:
        if tree.Draw(expression, selection, "goff") < 0:
            raise RuntimeError(f"Cannot evaluate ROOT expression: {expression}")

    # Count events for mass: use the two leading selected muons, without charge pairing.
    for event in dt:
        muons = sorted([mu for mu in event.Muon if mu.PT > 10 and abs(mu.Eta) < 2.4],
                       key=lambda mu: mu.PT, reverse=True)
        if len(muons) >= 2:
            md.Fill((muons[0].P4() + muons[1].P4()).M())
    for event in pt:
        pts = list(getattr(event, "Muons.PT"))
        etas = list(getattr(event, "Muons.Eta"))
        phis = list(getattr(event, "Muons.Phi"))
        isos = list(getattr(event, "Muons.IsolationVar"))
        indices = sorted([i for i in range(len(pts))
                          if pts[i] > 10 and abs(etas[i]) < 2.4 and isos[i] < 0.25],
                         key=lambda i: pts[i], reverse=True)
        if len(indices) >= 2:
            pair = []
            for index in indices[:2]:
                vector = ROOT.TLorentzVector()
                vector.SetPtEtaPhiM(pts[index], etas[index], phis[index], 0.105658)
                pair.append(vector)
            mp.Fill((pair[0] + pair[1]).M())

    # Save raw counts before normalising to unit area within the plotted range.
    counts = {
        "selected_muon_objects": {"truth": int(ht.GetEntries()),
                                  "Delphes": int(hd.GetEntries()),
                                  "Parnassus": int(hp.GetEntries())},
        "selected_leading_dimuon_events": {"Delphes": int(md.GetEntries()),
                                           "Parnassus": int(mp.GetEntries())},
        "dimuon_mass_mean_in_plot_range_GeV": {"Delphes": md.GetMean(),
                                               "Parnassus": mp.GetMean()},
    }
    for hist in histograms:
        integral = hist.Integral()
        if integral <= 0:
            raise RuntimeError(f"No selected entries in plotting range: {hist.GetName()}")
        hist.Scale(1.0 / integral)
        hist.SetDirectory(0)
    return histograms, counts


def overlay(ROOT, histograms, labels, colours, destination):
    canvas = ROOT.TCanvas("comparison", "comparison", 900, 650)
    legend = ROOT.TLegend(0.58, 0.72, 0.89, 0.89)
    histograms[0].SetMaximum(1.25 * max(hist.GetMaximum() for hist in histograms))
    for index, (hist, label, colour) in enumerate(zip(histograms, labels, colours)):
        hist.SetLineColor(colour)
        hist.SetLineWidth(2)
        hist.Draw("hist" if index == 0 else "hist same")
        legend.AddEntry(hist, label, "l")
    legend.Draw()
    for suffix in (".png", ".pdf"):
        canvas.SaveAs(str(destination.with_suffix(suffix)))
    canvas.Close()


def main():
    args = arguments()
    try:
        import ROOT
    except ImportError as error:
        raise RuntimeError("PyROOT is unavailable; source env.sh and activate .venv first") from error
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    project = Path(os.environ.get("DETECTOR_HOME", Path.cwd()))
    library = project / "tools/delphes/libDelphes.so"
    if not library.is_file() or ROOT.gSystem.Load(str(library)) < 0:
        raise RuntimeError(f"Cannot load Delphes classes: {library}; source env.sh first")

    products = [args.out / name for name in ("comparison_histograms.root", "counts.json",
                "muon_pt.png", "muon_pt.pdf", "dimuon_mass.png", "dimuon_mass.pdf")]
    if any(product.resolve() == source.resolve()
           for product in products for source in (args.delphes, args.parnassus)):
        raise RuntimeError("Output paths must not overwrite input ROOT files")
    fd, dt = open_tree(ROOT, args.delphes, "Delphes", ["Particle", "Muon"])
    fp, pt = open_tree(ROOT, args.parnassus, "Parnassus",
                       ["Muons.PT", "Muons.Eta", "Muons.Phi", "Muons.IsolationVar"])
    try:
        events = {"Delphes": int(dt.GetEntries()), "Parnassus": int(pt.GetEntries())}
        if any(number != args.expect for number in events.values()):
            raise RuntimeError(f"Expected {args.expect} events per tree; found {events}")
        histograms, counts = fill_histograms(ROOT, dt, pt)
    finally:
        fd.Close()
        fp.Close()

    counts["events"] = events
    counts["selected_leading_dimuon_fraction"] = {
        tool: counts["selected_leading_dimuon_events"][tool] / number
        for tool, number in events.items()}
    counts["inputs"] = {"Delphes": str(args.delphes.resolve()),
                        "Parnassus": str(args.parnassus.resolve())}
    counts["selection"] = "pT>10 GeV, |eta|<2.4; Parnassus IsolationVar<0.25"
    counts["normalisation"] = "Unit area within each plotting range; no cross-section scaling"
    args.out.mkdir(parents=True, exist_ok=True)
    colours = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kRed + 1]
    overlay(ROOT, histograms[:3], ["Stable truth", "Delphes CMS", "Parnassus CMS parametric"],
            colours, args.out / "muon_pt")
    overlay(ROOT, histograms[3:], ["Delphes CMS", "Parnassus CMS parametric"],
            colours[1:], args.out / "dimuon_mass")
    output = ROOT.TFile.Open(str(args.out / "comparison_histograms.root"), "RECREATE")
    if not output or output.IsZombie():
        raise RuntimeError(f"Cannot create histogram ROOT file in {args.out}")
    for hist in histograms:
        hist.Write()
    output.Close()
    (args.out / "counts.json").write_text(json.dumps(counts, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(counts, indent=2))
    print(f"Saved two plots (PNG/PDF), five ROOT histograms and counts.json to {args.out}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        raise SystemExit(f"ERROR: {error}")
