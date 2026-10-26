# 第三方来源与许可范围

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md)

核对日期：2026-10-15。本独立教学仓库使用下列项目，软件、模型与科学方法的贡献仍属于相应项目；本说明不代替许可证，也不表示这些项目为本教程背书。

## 安装时从上游获取的软件

| 组件 | 本次版本 | 来源与许可范围 |
|---|---|---|
| MadGraph5_aMC@NLO，MadTeam | 2.9.27，`eb76cab72b8d44aac7162ac7221ac08a4384a169` | [源码许可](https://github.com/mg5amcnlo/mg5amcnlo/blob/eb76cab72b8d44aac7162ac7221ac08a4384a169/LICENSE)，改编自 Illinois/NCSA；vendor 组件另有许可 |
| PYTHIA / pythia8mc，Pythia 8 Team | `pythia8mc==8.316.0` | [发行包](https://pypi.org/project/pythia8mc/8.316.0/)，GPL v2 或以后版本 |
| Delphes，UCL/CERN 及贡献者 | 3.5.1，`28658365abeb71ee36dfc739f9670c1514c0cb10` | [软件许可](https://github.com/delphes/delphes/blob/28658365abeb71ee36dfc739f9670c1514c0cb10/LICENSE)，GPL v3 或以后版本；网站文档另采用 CC BY-SA 4.0 |
| Parnassus，Dmitrii Kobylianskii 及贡献者 | `c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865` | [MIT 许可](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/LICENSE)，Copyright (c) 2025 Dmitrii Kobylianskii |
| ROOT / PyROOT，ROOT 团队 | ROOT 6.40.00，wheel `0.1a12` | [LGPL 2.1 或以后版本](https://root.cern/about/license/)，可选附带组件可能另有许可 |
| pyhepmc，Hans Dembinski 及贡献者 | 2.16.1 | [BSD-3-Clause 许可](https://github.com/scikit-hep/pyhepmc/blob/0d9ed0adbeab5a812e43c1bf01c89b45cb93d5d8/LICENSE)；其 HepMC3 库采用 LGPL v3 |
| FastJet 与 Scikit-HEP FastJet 绑定 | Python wheel 3.5.2.0 | [Python 绑定](https://github.com/scikit-hep/fastjet) 为 BSD-3-Clause；底层 FastJet C++ 库为 GPL v2 或以后版本 |

CPU PyTorch 等其他 Python 依赖保留各自许可。安装时将它们下载到本地环境；版本见 [requirements.lock.txt](../requirements.lock.txt)，许可见安装包自带文件。论文引用不能代替使用许可。

## 本仓库实际发布的材料

手册与说明图是独立编写的教学整理。`hepmc_io.py` 是调用 Pythia/pyhepmc 公开 API 的自有格式适配层；`plot.py` 是调用 ROOT API 的自有分析脚本。它们不包含上游生成器、探测器模型或复制的教程分析实现。`config/shower.cmnd` 和 `config/parnassus.yaml` 只填写所说明接口的设置。

图、数值验证记录及 `examples/comparison_histograms.root` 内的五条 `TH1D` 来自本地模拟。ROOT 示例只有直方图，不含完整探测器事件树或嵌入源码/宏。这些小样本结果不代表与完整探测器模拟等价。

Delphes CMS Tcl 卡在本地从固定版本源码复制，并添加一条随机种子设置。该卡、上游源码仓库、`.venv`、编译程序、LHE/HepMC 和完整探测器 ROOT 树均不纳入公开仓库。读者从原项目获取软件，并保留其自带许可证。

[SMEFTsim 学习教程](https://github.com/RuneTan/smeftsim-learning) 提供了分步教学方式的参考，不是本项目的安装依赖。本仓库不附带 Ilaria Brivio 独立教程中的文件，也不借用其他项目的许可覆盖它们。外部教程正文和图片采用链接引用，不在这里复制；实际参考的页面及固定版本见 [SOURCES](SOURCES.zh-CN.md)。

## 科学引用

研究中使用这些工具时，请查看项目当时的引用要求，并引用所用的方法，例如：

- C. Bierlich 等，[PYTHIA 8.3 物理与使用指南](https://arxiv.org/abs/2203.11601)，arXiv:2203.11601。
- J. de Favereau 等，[DELPHES 3](https://arxiv.org/abs/1307.6346)，JHEP 02 (2014) 057，[DOI](https://doi.org/10.1007/JHEP02%282014%29057)。
- A. Elabd、E. Gross、D. Kobylianskii、B. Nachman，[Parnassus](https://arxiv.org/abs/2606.26089)，arXiv:2606.26089。
- J. Alwall 等，[MadGraph5_aMC@NLO](https://arxiv.org/abs/1405.0301)，arXiv:1405.0301。
- A. Buckley 等，[HepMC3 事件记录库](https://arxiv.org/abs/1912.08005)，arXiv:1912.08005。
- M. Cacciari、G. P. Salam、G. Soyez，[FastJet 使用手册](https://arxiv.org/abs/1111.6097)，arXiv:1111.6097。
- R. Brun、F. Rademakers，ROOT 框架，见[项目引用说明](https://github.com/root-project/root#cite)。

## 项目自有材料

本项目尚未为自有材料选择统一再使用许可证。公开可见不等于整个仓库采用 MIT；第三方权利及其许可范围保持独立。
