# 依赖关系与环境隔离

[English](dependencies.md)

本教程建立一套项目独立的 Linux 环境。Python、科学软件包、MadGraph 和 Delphes 安装在 `~/detector-learning` 内；Ubuntu 和系统编译器由 Linux 提供。不需要先安装另一个 SMEFTsim 教程。

## 1. 只看新项目

下图的箭头表示“运行或构建需要”，不是模拟数据流：

```mermaid
flowchart TB
    OS["系统：Ubuntu 22.04 / Linux x86-64"]
    COMP["系统工具：GCC / G++ / gfortran / make"]
    subgraph PROJECT["~/detector-learning：项目自己的文件"]
        BASE["tools/python：Python 3.12.12 基础解释器"]
        ENV[".venv：唯一 Python 虚拟环境"]
        MG["tools/mg：MadGraph 源码"]
        DEL["tools/delphes：Delphes 源码和 C++ 程序"]
        ROOT[".venv 包：ROOT / PyROOT 6.40.00"]
        PYTHIA[".venv 包：pythia8mc + pyhepmc"]
        PAR[".venv 包：Parnassus + CPU PyTorch + FastJet + uproot"]
        PLOT["scripts/plot.py：调用 ROOT 分析和画图"]
        UV["tools/uv：安装工具，运行模拟不需要它"]
    end
    BASE --> OS
    ENV --> BASE
    COMP --> OS
    MG --> ENV
    MG --> COMP
    DEL --> COMP
    DEL --> ROOT
    ROOT --> ENV
    PYTHIA --> ENV
    PAR --> ENV
    PLOT --> ROOT
```

Parnassus 通过 `uproot` 写 ROOT 格式文件，本身不依赖 PyROOT。ROOT 在这里承担 Delphes 构建和交互分析；把它装进同一环境，是为了让你始终使用同一个 `python`。

Delphes 自带 FastJet/Tcl 的 C++ 源码；Parnassus 使用 Python 的 FastJet wheel。它们分别服务于两个后端，不需要另外编译第三套 FastJet。

## 2. 哪些是系统、环境、软件包

| 层次 | 实际位置 | 作用 |
|---|---|---|
| Linux 系统 | 原生或 WSL 2 中的 Ubuntu 22.04 | 提供内核接口、基础共享库和终端；不要求特定的发行版名称或 Linux 用户名 |
| 系统工具 | `/usr/bin` 等 | Git、下载工具和编译器；两个项目都可以使用 |
| Python 基础解释器 | `tools/python/cpython-3.12.12-linux-x86_64-gnu` | `.venv` 所依赖的项目内 Python，不能只复制 `.venv` 后删掉它 |
| Python 环境 | `.venv` | 隔离本项目的第三方 Python 包；不包含系统级编译器 |
| Python 包及其预编译库 | `.venv/lib/python3.12/site-packages` | ROOT、Pythia、HepMC、Parnassus、PyTorch 等；版本见 [锁文件](../requirements.lock.txt) |
| 源码及编译程序 | `tools/mg`、`tools/delphes` | MadGraph 用 Python 驱动生成并编译 Fortran；Delphes 编译为 C++ 程序 |
| 安装工具 | `tools/uv/bin/uv` | 下载 Python、创建环境和安装依赖 |
| 图形兼容库 | `.venv/local-libs` | 从 Ubuntu 包提取的 libSM/libICE；仅供本项目 ROOT 加载 |
| 输入设置与产物 | `config`、`work/dy`、`out` | 卡、生成过程和模拟结果，属于数据而不是环境 |

`scripts/env.sh` 为当前终端指向这些位置；`source .venv/bin/activate` 使提示符显示环境。MadGraph、Pythia、Parnassus 和 ROOT 的 Python 操作都用 `python`，不用在 Python 3.10 和 3.12 之间切换。

命令使用相对项目根目录的路径。`tools/mg` 保存 MadGraph，`work/dy` 保存导出的过程，`out` 保存生成数据。安装指南和手册会明确创建这些目录。

## 3. 为什么可以统一到 Python 3.12

Parnassus 固定版本要求 Python `>=3.12,<3.13`；[ROOT 0.1a12](https://pypi.org/project/ROOT/0.1a12/) 提供对应的 CPython 3.12 Linux wheel。Python 扩展包必须匹配解释器版本，所以这里单独安装该 wheel，不能把旧 Python 3.10 的 ROOT 目录接到新环境中。

参考的 200 事件 SM LO 双 Muon 样本由 MadGraph 2.9.27 在 Python 3.12 下生成。旧源码可能出现 `SyntaxWarning: invalid escape sequence`；消除警告本身不能证明运行成功。其他模型、NLO 计算和插件需要单独验证。

按 [安装指南](setup.zh-CN.md) 使用本项目 ROOT 编译 Delphes，并用 `ldd` 核对库路径；只修改文档或 Python 命令不会重新链接二进制程序。

## 4. 不同项目之间的边界

每个项目使用独立目录和环境。切换项目时打开新的 Linux 终端，再加载对应项目的环境设置，避免借用其他项目的 Python 包或共享库。

不需要第二套 Linux 系统。Windows 读者可使用已安装的 WSL 2 Ubuntu，原生 Linux 读者使用现有系统。WSL 的虚拟磁盘承载整个 Linux 文件系统，普通项目清理不应移动或删除该磁盘文件。

## 5. 已验证的范围

参考运行记录完成了 MadGraph → Pythia → 两种探测器后端 → ROOT 绘图，各阶段均有 200 个事件。同一后端在相同输入和种子下重放，Muon pT 数值一致；转换前后的稳定粒子四动量和产生位置保持一致。

[参考记录](../examples/validation.json) 保存了版本与数值，描述的是一次已记录的运行，不代表你的机器已经配置完成。请实际完成安装检查和手册。完整安装尚未在另一台干净机器从头重放；物理比较仍属于小样本接口练习。