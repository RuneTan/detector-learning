# 探测器模拟链学习

[English](README.md)

一份手动完成 **MadGraph → Pythia → Delphes / Parnassus** 的教程。沿着一个小样本理解硬散射、shower、探测器响应与分析，再逐项改变设置并检查结果。

## 从哪里开始

仓库提供教学文件和小型参考结果。**克隆仓库不会自动安装 Linux、Python 或模拟软件。**

| 你的起点 | 下一步 |
|---|---|
| Windows，尚未安装 Linux | 按 [安装指南](docs/setup.zh-CN.md) 准备 WSL 2 和 Ubuntu，再在 Ubuntu 终端中继续 |
| 已有原生 Linux 或 WSL 2 Ubuntu | 按 [安装指南](docs/setup.zh-CN.md) 安装本项目环境和工具 |
| 已完成安装检查 | 按 [学习手册](docs/handbook.zh-CN.md) 生成事件并运行探测器链 |
| 只想浏览已有图 | 查看 [参考结果](examples/README.zh-CN.md) |

文档使用的平台是 x86-64 Ubuntu 22.04，可原生运行或置于 WSL 2 中。SMEFTsim 学习仓库是 [相关教程](https://github.com/RuneTan/smeftsim-learning)，不需要先安装它。

完成安装后，在 **Linux Bash** 中逐条执行：

```bash
cd ~/detector-learning
source scripts/env.sh
source .venv/bin/activate
```

接着从 [手册第 3 节](docs/handbook.zh-CN.md#3-madgraph准备硬散射输入) 开始，先生成分析需要的输入。两份探测器 ROOT 文件都生成后，再运行：

```bash
python scripts/plot.py
```

它读取 `out/delphes.root` 和 `out/parnassus.root`，检查事件数，将图、直方图和计数写入 `out/plots`。

## 仓库结构

| 位置 | 内容 |
|---|---|
| [docs](docs/README.md) | 安装指南、学习手册、依赖、来源与第三方声明 |
| [scripts](scripts/README.zh-CN.md) | 环境设置、ROOT 分析及 Pythia/HepMC 格式适配 |
| [config](config) | Pythia 与 Parnassus 设置；Delphes 卡的获取方式见安装指南 |
| [examples](examples/README.zh-CN.md) | 小型参考图、直方图和验证记录 |
| `bin/root-config` | 固定版本 ROOT wheel 的编译辅助工具 |
| `requirements.lock.txt` | 固定 Python 依赖 |
| `tools`、`.venv`、`work`、`out` | 安装或运行时创建，Git 不收录 |

除明确切换目录的步骤外，文档命令均从项目根目录运行。Windows 读者应先打开已安装的 Ubuntu，再输入 Linux 命令。

## 示例与范围

参考练习使用 13 TeV 下的 200 个 SM Drell–Yan 事件，过程为 `p p > mu+ mu-`。Delphes 和 Parnassus 读取同一份 HepMC3 输入。Parnassus 使用 CPU 参数化 CMS 响应；本练习不训练或验证神经探测器模型。

![稳定 truth 与重建 Muon 横动量](examples/muon_pt.png)

图在绘图区间内归一化，用于比较形状。计数和限制见 [参考结果](examples/README.zh-CN.md)。仓库不分发完整原始事件，请按手册生成自己的输入。

这是学习与接口验证项目。署名与许可范围见 [第三方声明](docs/THIRD_PARTY_NOTICES.zh-CN.md)；自有文件尚未选择统一再使用许可证。
