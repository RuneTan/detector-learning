# Tutorial scripts

[简体中文](README.zh-CN.md) · [Project overview](../README.md)

Complete [setup](../docs/setup.md) first. Run commands from the project root in Linux Bash.

| File | Role |
|---|---|
| [env.sh](env.sh) | Source project-local interpreter, library and build-tool paths for the current terminal |
| [plot.py](plot.py) | Read existing Delphes/Parnassus ROOT files and produce figures, histograms and counts |
| [hepmc_io.py](hepmc_io.py) | Convert an in-memory Pythia event to HepMC3 and check stable-particle transfer |

```bash
source scripts/env.sh
source .venv/bin/activate
python scripts/plot.py --help
```

After generating the detector outputs:

```bash
python scripts/plot.py --delphes out/delphes.root --parnassus out/parnassus.root --out out/plots --expect 200
```

The handbook imports `to_hepmc` with `from scripts.hepmc_io import to_hepmc` from the project root. The adapter itself does not run an event loop or detector simulation.

The [handbook](../docs/handbook.md) explains the package calls; these helpers do not install Linux or simulation software.
