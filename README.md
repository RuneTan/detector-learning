# Detector-chain learning

[简体中文](README.zh-CN.md)

A hands-on **MadGraph → Pythia → Delphes / Parnassus** tutorial. Follow a small event sample from hard scattering to detector output, change one setting at a time, and inspect the results with ROOT.

## Start here

This repository contains teaching files and small reference results. Cloning it does **not** install Linux, Python or the simulation packages.

| Your starting point | Next step |
|---|---|
| Windows without Linux | Follow [setup](docs/setup.md) to install WSL 2 and Ubuntu, then continue in the Ubuntu terminal |
| Native Linux or an existing WSL 2 Ubuntu | Follow [setup](docs/setup.md) to install this project's environment and tools |
| Installation checks completed | Follow the [handbook](docs/handbook.md) to generate events and run the detector chain |
| Only browsing the supplied figures | Open [reference results](examples/README.md) |

The documented platform is x86-64 Ubuntu 22.04, either native or under WSL 2. The SMEFTsim learning repository is a [related tutorial](https://github.com/RuneTan/smeftsim-learning), not an installation prerequisite.

After completing setup, run these commands in **Linux Bash**:

```bash
cd ~/detector-learning
source scripts/env.sh
source .venv/bin/activate
```

Then start [handbook section 3](docs/handbook.md#3-madgraph-prepare-the-hard-scattering-input). Generate the inputs before running the analysis. Once both detector ROOT files exist:

```bash
python scripts/plot.py
```

This reads `out/delphes.root` and `out/parnassus.root`, checks their event counts, and writes figures, histograms and counts into `out/plots`.

## Repository layout

| Location | Contents |
|---|---|
| [docs](docs/README.md) | Installation, handbook, dependencies, sources and third-party notices |
| [scripts](scripts/README.md) | Environment settings, ROOT analysis and the Pythia/HepMC adapter |
| [config](config) | Pythia and Parnassus settings; setup explains how to obtain a Delphes card |
| [examples](examples/README.md) | Small reference figures, histograms and validation records |
| `bin/root-config` | Build helper for the pinned ROOT wheel |
| `requirements.lock.txt` | Pinned Python dependencies |
| `tools`, `.venv`, `work`, `out` | Created during installation or execution; excluded from Git |

All commands in the guides run from the project root unless a step explicitly changes directory. On Windows, open your installed Ubuntu distribution before using Linux commands.

## Example and scope

The reference exercise uses 200 SM Drell–Yan events, `p p > mu+ mu-`, at 13 TeV. Delphes and Parnassus read the same HepMC3 input. Parnassus uses a CPU parametric CMS response; this exercise does not train or validate a neural detector model.

![Stable truth and reconstructed muon transverse momentum](examples/muon_pt.png)

The figure compares shapes normalized within the plotted range. Counts and limitations are explained in [examples](examples/README.md). Raw event samples are not distributed; generate your own using the handbook.

This is a learning and interface-validation project. [Third-party notices](docs/THIRD_PARTY_NOTICES.md) describe attribution and license boundaries; no project-wide reuse license has been selected.
