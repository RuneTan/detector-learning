# 教程辅助脚本

[English](README.md) · [项目说明](../README.zh-CN.md)

先完成 [安装指南](../docs/setup.zh-CN.md)。下列命令在项目根目录的 Linux Bash 中执行。

| 文件 | 用途 |
|---|---|
| [env.sh](env.sh) | 为当前终端设置本项目的解释器、库和编译工具路径 |
| [plot.py](plot.py) | 读取已生成的 Delphes/Parnassus ROOT 文件，生成图、直方图和计数 |
| [hepmc_io.py](hepmc_io.py) | 将内存中的 Pythia 事件转为 HepMC3，并检查稳定粒子传递 |

```bash
source scripts/env.sh
source .venv/bin/activate
python scripts/plot.py --help
```

生成两份探测器输出后，可以运行：

```bash
python scripts/plot.py --delphes out/delphes.root --parnassus out/parnassus.root --out out/plots --expect 200
```

手册在项目根目录使用 `from scripts.hepmc_io import to_hepmc` 导入转换函数。适配模块本身不运行事件循环或探测器模拟。

包的实际调用见 [学习手册](../docs/handbook.zh-CN.md)；这些脚本不负责安装 Linux 或模拟软件。
