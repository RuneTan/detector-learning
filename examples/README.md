# Local validation examples

[简体中文](README.zh-CN.md)

These results come from a local 200-event SM Drell–Yan exercise on 2026-10-14. The full chain was checked again with the independent Python 3.12 environment: hard-event contents and the HepMC input checksum matched the original baseline, as did selection counts and histograms. [validation.json](validation.json) records settings, event counts and environment versions; [SOURCES.md](../docs/SOURCES.md) records versions and provenance.

| File | Contents |
|---|---|
| `muon_pt.png`, `muon_pt.pdf` | Muon pT shapes for stable truth, Delphes and Parnassus |
| `dimuon_mass.png`, `dimuon_mass.pdf` | Leading-dimuon mass for the two reconstructed responses |
| `comparison_histograms.root` | The five normalized histograms for inspection in ROOT |
| `validation.json` | Inputs, seeds, cuts, cross section, counts and repeatability checks |

Plots are normalized within the specified plotting range. Their areas do not preserve acceptance; calculate acceptance from raw counts. The curves show central values, and 200 events cannot validate detailed detector performance. Particle-flow, efficiency and isolation implementations differ between backends, so exact agreement is not required.

From the Linux project root, `python scripts/plot.py` analyzes your `out/delphes.root` and `out/parnassus.root`, writing to `out/plots`; `counts.json` preserves unnormalized counts. After completing setup and generating your own detector outputs, run:

```bash
source scripts/env.sh
source .venv/bin/activate
python scripts/plot.py --delphes out/delphes.root --parnassus out/parnassus.root --out out/plots
```

Those two raw detector files are not distributed in the repository. The script has been checked bin by bin against the five reference histograms below, including contents, errors and entries; selection and normalization definitions match.

![Muon pT](muon_pt.png)

![Leading-dimuon mass](dimuon_mass.png)

To inspect only the supplied histograms, start Python with ROOT from the Linux project root:

```bash
source scripts/env.sh
source .venv/bin/activate
python
```

At `>>>`, enter each line and press Enter:

```python
import ROOT
ROOT.gROOT.SetBatch(True)
f = ROOT.TFile.Open("examples/comparison_histograms.root")
f.ls()
h = f.Get("htruth")
print(h.Integral())
f.Close()
exit()
```

`htruth`, `hdelphes` and `hparna` belong to the pT plot; `dimuon_delphes` and `dimuon_parna` to the mass plot. Each integral should be approximately 1. Full LHE/HepMC files and detector trees are excluded because readers can generate them in Linux following the handbook.
