# Third-party sources and license scope

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md)

Checked on 2026-10-15. This independent teaching repository uses the projects below. Their software, models and scientific methods remain credited to the respective projects; this notice does not replace their licenses or imply their endorsement.

## Software obtained during installation

| Component | Version used | Source and license scope |
|---|---|---|
| MadGraph5_aMC@NLO, MadTeam | 2.9.27, `eb76cab72b8d44aac7162ac7221ac08a4384a169` | [Source license](https://github.com/mg5amcnlo/mg5amcnlo/blob/eb76cab72b8d44aac7162ac7221ac08a4384a169/LICENSE), adapted from Illinois/NCSA; vendor components have their own terms |
| PYTHIA / pythia8mc, Pythia 8 Team | `pythia8mc==8.316.0` | [Distribution](https://pypi.org/project/pythia8mc/8.316.0/), GPL v2 or later |
| Delphes, UCL/CERN and contributors | 3.5.1, `28658365abeb71ee36dfc739f9670c1514c0cb10` | [Software license](https://github.com/delphes/delphes/blob/28658365abeb71ee36dfc739f9670c1514c0cb10/LICENSE), GPL v3 or later; website documentation is separately CC BY-SA 4.0 |
| Parnassus, Dmitrii Kobylianskii and contributors | `c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865` | [MIT license](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/LICENSE), Copyright (c) 2025 Dmitrii Kobylianskii |
| ROOT / PyROOT, ROOT team | ROOT 6.40.00, wheel `0.1a12` | [LGPL 2.1 or later](https://root.cern/about/license/); optional bundled components can have other terms |
| pyhepmc, Hans Dembinski and contributors | 2.16.1 | [BSD-3-Clause license](https://github.com/scikit-hep/pyhepmc/blob/0d9ed0adbeab5a812e43c1bf01c89b45cb93d5d8/LICENSE); its HepMC3 library has LGPL v3 terms |
| FastJet and Scikit-HEP FastJet bindings | Python wheel 3.5.2.0 | [Python bindings](https://github.com/scikit-hep/fastjet), BSD-3-Clause; the underlying FastJet C++ library is GPL v2 or later |

Other Python dependencies, including CPU PyTorch, retain their own licenses. The installation downloads them into the local environment; see [requirements.lock.txt](../requirements.lock.txt) and their installed license files. A citation is not a substitute for a license.

## Material included here

The handbook and explanatory diagrams are independently written teaching notes. `scripts/hepmc_io.py` is an original adapter using public Pythia/pyhepmc APIs; `scripts/plot.py` is an original analysis script using ROOT APIs. They do not include an upstream generator, detector model or copied tutorial analysis implementation. `config/shower.cmnd` and `config/parnassus.yaml` contain settings for the documented interfaces.

The figures, numerical validation record and five `TH1D` objects in `examples/comparison_histograms.root` were produced by local simulations. The ROOT example contains histograms, not detector event trees or embedded source/macros. These small-sample results do not establish equivalence to full detector simulation.

The Delphes CMS Tcl card is copied locally from the pinned Delphes source and receives one random-seed setting. The card, upstream source repositories, `.venv`, compiled programs, LHE/HepMC files and full detector ROOT trees are excluded from the public repository. Readers obtain the software from its original projects, retaining the license files supplied there.

The [SMEFTsim learning tutorial](https://github.com/RuneTan/smeftsim-learning) informed the stepwise teaching approach; it is not an installation dependency. Files from Ilaria Brivio's independent tutorial are not bundled here. External tutorial prose and figures are referenced rather than reproduced; practical sources and fixed versions are listed in [SOURCES.md](SOURCES.md).

## Scientific references

For research using these tools, consult the projects' current citation instructions and cite the relevant methods, for example:

- C. Bierlich et al., [PYTHIA 8.3 physics and usage guide](https://arxiv.org/abs/2203.11601), arXiv:2203.11601.
- J. de Favereau et al., [DELPHES 3](https://arxiv.org/abs/1307.6346), JHEP 02 (2014) 057, [DOI](https://doi.org/10.1007/JHEP02%282014%29057).
- A. Elabd, E. Gross, D. Kobylianskii and B. Nachman, [Parnassus](https://arxiv.org/abs/2606.26089), arXiv:2606.26089.
- J. Alwall et al., [MadGraph5_aMC@NLO](https://arxiv.org/abs/1405.0301), arXiv:1405.0301.
- A. Buckley et al., [HepMC3 event record library](https://arxiv.org/abs/1912.08005), arXiv:1912.08005.
- M. Cacciari, G. P. Salam and G. Soyez, [FastJet user manual](https://arxiv.org/abs/1111.6097), arXiv:1111.6097.
- R. Brun and F. Rademakers, ROOT framework; see the [project citation guidance](https://github.com/root-project/root#cite).

## Project-owned material

No project-wide reuse license has been selected for this repository's own material. Public availability does not grant an MIT license to the complete repository. Third-party rights and license scopes remain separate.
