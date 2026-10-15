# Sources, pinned versions and implementation scope

[简体中文](SOURCES.zh-CN.md)

The teaching route draws on [smeftsim-learning](https://github.com/RuneTan/smeftsim-learning): stepwise inputs, an isolated environment, ROOT analysis, and small-sample checks before larger runs. It is a teaching reference, not an installation or runtime dependency.

| Source | Version used here | Use in this tutorial |
|---|---|---|
| [Pythia 8 manual](https://pythia.org/latest-manual/Frontpage.html) and [worksheet](https://pythia.org/download/pdf/worksheet8312.pdf) | `pythia8mc==8.316.0`, fixed for this tutorial | LHE input, ISR/FSR/MPI, hadronization, decays and event records |
| [pyhepmc reference](https://scikit-hep.org/pyhepmc/reference.html) and [basic I/O](https://scikit-hep.org/pyhepmc/examples/basics.html) | Version in the dependency lock file | `GenEvent.from_hepevt`, GeV/mm and HepMC3 ASCII |
| [Delphes Quick Tour](https://delphes.github.io/workbook/quick-tour/) and [DESY tutorial](https://delphes.github.io/tutorials/prefit/) | 3.5.1, commit `28658365abeb71ee36dfc739f9670c1514c0cb10` | HepMC → ROOT, CMS card, branches and analysis |
| [Delphes source](https://github.com/delphes/delphes/tree/3.5.1) | Build only `DelphesHepMC3`, the shared library and required dictionaries | Check actual reader event counts; leave source unchanged |
| [Parnassus](https://github.com/parnassus-hep/parnassus) | Commit `c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865` | Unified API, parametric CMS response, HepMC input and ROOT output |
| [Parnassus parametric mode](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/parametric-mode.md) | CPU, PyTorch 2.7.1+cpu | The mode exercised and checked here |
| [Parnassus neural mode](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/neural-mode.md) | Not run here | Background on parametric and learned responses |
| [MadGraph](https://github.com/mg5amcnlo/mg5amcnlo/tree/v2.9.27) | 2.9.27, commit `eb76cab72b8d44aac7162ac7221ac08a4384a169` | Independent source tree; SM Drell–Yan generation with this project's Python 3.12 |
| [MadGraph run-card definitions](https://github.com/mg5amcnlo/mg5amcnlo/blob/eb76cab72b8d44aac7162ac7221ac08a4384a169/madgraph/various/banner.py) | Same pinned version; MLM display block hidden by default, `ickkw=0`, `xqcut=0` | Matching/merging defaults; the negative `ptlmax` convention was also checked in `Template/LO/SubProcesses/cuts.f` and `setcuts.f` |
| [Parnassus CLI](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/cli-reference.md) and [pipelines](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/pipelines.md) | Same pinned version | Overrides, batch size, clustering, isolation variables and output branches |
| [ROOT wheel](https://pypi.org/project/ROOT/0.1a12/) | ROOT 6.40.00; wheel `0.1a12`, CPython 3.12 Linux x86-64 build | Project-local `.venv`; Delphes compilation, tree reading and plotting |
| [uv Python management](https://docs.astral.sh/uv/guides/install-python/) | uv 0.9.28, Python 3.12.12 | Project-local Python without changing a global installation |

## Keeping the components small

All Python work uses this project's Python 3.12 environment. Parnassus already installs the Pythia Python wheel, so no separate C++ Pythia is installed. pyhepmc supplies HepMC3, avoiding a standalone HepMC build. Delphes uses its bundled FastJet/Tcl and only the necessary build targets. Parnassus uses its upstream runtime dependencies, without development extras, GPU/CUDA packages or a new detector implementation.

The interface helpers are `env.sh`, `bin/root-config` and `hepmc_io.py`. A single `plot.py` concentrates ROOT reading, selections, plotting and counts, keeping the handbook focused on package calls and event flow. It only analyzes existing outputs; it does not replace generation, showering or detector simulation, add dependencies, or introduce a separate plotting framework.

`hepmc_io.py` is a thin adapter written for this project using upstream APIs; it does not copy Parnassus's conversion algorithm. It makes vertex encoding explicit and checks stable-particle counts and four-momenta event by event. It does not claim complete validation of every multigeneration Pythia decay topology, nor does it propagate SMEFT multiweights. LHE/Pythia supply the original event record; research extensions require further history and weight checks.

## Licenses and attribution

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for component attribution, license scope and scientific references. Consult the license files in each pinned source tree and its dependencies for the controlling terms.

This teaching repository does not redistribute those third-party source trees, installed environments or the original CMS Tcl card. Readers obtain them from upstream and retain their LICENSE/COPYING files. `config/delphes_CMS.tcl` is copied locally from the upstream card with a fixed seed added.

`config/parnassus.yaml` contains this exercise's settings entered through the published upstream configuration interface. Figures and numbers were generated locally. The listed projects and their contributors retain credit for the models, generators, detector implementations and methods. This tutorial contributes independent operating instructions and interface exercises. No project-wide reuse license has yet been selected for its own documentation and helpers.

These checks do not establish full CMS simulation, exact equivalence of the two CMS responses, neural-model validation, SMEFT reweighting closure or successful cluster execution.
