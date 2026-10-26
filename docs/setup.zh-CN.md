# 独立 Linux 安装与重新构建

[English](setup.md)

当前机器已经完成安装和运行校验，直接使用 [handbook](handbook.zh-CN.md)。这页给新机器或需要重建环境的读者使用；**不需要先安装 SMEFTsim 教程**。依赖层次见 [dependencies.md](dependencies.zh-CN.md)。

固定路线：x86-64 Ubuntu 22.04、项目内 Python 3.12.12、一个 `.venv`，以及本项目自己的 MadGraph、ROOT、Pythia、Delphes 和 Parnassus。系统编译器由 Linux 提供，Python 与科学软件安装在项目目录。步骤不会修改 Windows Python 或原项目环境。

每行 Bash 命令完整输入后回车一次，等提示符回来再执行下一行。标记为 PowerShell 的命令才在 Windows 执行；文件内容在编辑器中修改。已有目录或环境时，检查版本并跳过创建步骤，不要重复覆盖。

## 1. 准备 Linux 系统

本机可继续使用现有 WSL 发行版 `SMEFTsim`，不需要创建第二块虚拟磁盘。

新 Windows 机器可按 [Microsoft WSL 安装指南](https://learn.microsoft.com/windows/wsl/install) 安装 Ubuntu 22.04。在管理员 **PowerShell** 中执行：

```powershell
wsl --install -d Ubuntu-22.04
```

按提示重启并启动 Ubuntu，设置自己的 Linux 用户名和密码。下面命令均在 **Linux Bash** 中执行。已经使用原生 Ubuntu 或已有 WSL Ubuntu 的读者跳过这一段。

首次准备系统工具：

```bash
sudo apt-get update
sudo apt-get install -y build-essential gfortran git curl ca-certificates perl nano
uname -m
g++ --version
gfortran --version
```

应看到 `x86_64` 和编译器版本。`sudo` 在这里仅安装 Linux 系统工具，不用它安装 Python 包；已经具备这些工具的本机不需重复安装。

## 2. 获取教学文件

在 Linux 文件系统内克隆，不放在 `/mnt/c`：

```bash
git clone https://github.com/RuneTan/detector-learning.git ~/detector-learning
cd ~/detector-learning
mkdir -p tools work out
source env.sh
```

目录已存在时跳过克隆，进入项目即可。`env.sh` 根据自己的位置确定项目根目录，将 Python 下载位置、uv 缓存和终端路径限定到本项目，不改 `.bashrc`。此时 Python/ROOT 尚未安装，后面的步骤会创建它们。

Windows 文件管理器可访问 `\\wsl.localhost\发行版名称\home\你的Linux用户名\detector-learning`。本机对应 `\\wsl.localhost\SMEFTsim\home\smeft\detector-learning`。

`enter-linux.ps1` 中的发行版名、用户名和 Linux 目录采用本机名称；在其他机器使用入口前，替换为自己的值。原生 Linux 不需要 Windows 入口。

## 3. 获取项目内 Python 和科学软件包

从 [uv 固定版本发布页](https://github.com/astral-sh/uv/releases/tag/0.9.28) 获取独立可执行文件，直接解包到项目内，不调用旧项目的 pip：

```bash
curl -fL https://github.com/astral-sh/uv/releases/download/0.9.28/uv-x86_64-unknown-linux-gnu.tar.gz -o tools/uv.tar.gz
mkdir -p tools/uv/bin
tar -xzf tools/uv.tar.gz --strip-components=1 -C tools/uv/bin uv-x86_64-unknown-linux-gnu/uv
tools/uv/bin/uv --version
tools/uv/bin/uv python install 3.12.12
tools/uv/bin/uv venv --python 3.12.12 .venv
source .venv/bin/activate
python --version
```

应看到 uv 0.9.28、Python 3.12.12。基础解释器在 `tools/python`，第三方包在 `.venv`；二者共同组成项目的 Python 运行环境。不要只移动或复制 `.venv`；换目录或机器时按这页重建。

本练习使用 CPU PyTorch。先安装 CPU wheel，再安装锁定依赖，其中已经包含 CPython 3.12 的 ROOT wheel：

```bash
tools/uv/bin/uv pip install --python .venv/bin/python torch==2.7.1+cpu --index-url https://download.pytorch.org/whl/cpu
tools/uv/bin/uv pip install --python .venv/bin/python -r requirements.lock.txt
```

锁文件记录运行依赖，Parnassus 本体在下一步从固定源码安装。不要运行 `uv sync --all-extras`，本练习不需要开发 extras、CUDA 包或神经模型训练工具。

ROOT wheel 的版本为 `0.1a12`，对应 ROOT 6.40.00；这是本教程固定并验证的构建，不代表 ROOT 网站当前最新版。wheel 提供 C++ ROOT 库、命令行程序和 PyROOT，不能复用其他 Python 小版本的 wheel。

本机的最小 Ubuntu 缺少 ROOT 绘图需要的 libSM/libICE。下面下载 Ubuntu 软件包并**提取到项目内**，不用 `sudo` 安装：

```bash
mkdir -p .venv/local-libs/debs
cd .venv/local-libs/debs
apt-get download libsm6 libice6
```

下面是一个 Bash 循环：第一行回车后会出现续行提示，第二行前两个空格只为了阅读；输入第三行 `done` 并回车后执行，不需要 Python 循环那样再空白回车：

```bash
for archive in *.deb; do
  dpkg-deb -x "$archive" ..
done
```

回到项目根目录：

```bash
cd ../../..
source env.sh
python -c "import ROOT, torch; print(ROOT.gROOT.GetVersion()); print(torch.__version__)"
```

应看到 ROOT 6.40.00、PyTorch 2.7.1+cpu。ROOT 第一次导入可能提示 wheel 处于 alpha 发布阶段；本教程使用已验证的小样本教学配置。

## 4. 从上游获取独立源码

目标目录已存在时跳过克隆，核对版本即可。下面都从上游下载，不从 `~/smeftsim` 复制或借用文件：

```bash
git clone --branch v2.9.27 --depth 1 https://github.com/mg5amcnlo/mg5amcnlo.git tools/mg
git clone --branch 3.5.1 --depth 1 https://github.com/delphes/delphes.git tools/delphes
git clone https://github.com/parnassus-hep/parnassus.git tools/parnassus
git -C tools/parnassus checkout c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865
git -C tools/mg rev-parse HEAD
git -C tools/delphes rev-parse HEAD
git -C tools/parnassus rev-parse HEAD
```

三个 commit 应分别为：

- MadGraph：`eb76cab72b8d44aac7162ac7221ac08a4384a169`。
- Delphes：`28658365abeb71ee36dfc739f9670c1514c0cb10`。
- Parnassus：`c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865`。

安装 Parnassus；运行依赖已由锁文件安装，所以这次不再解析升级依赖：

```bash
tools/uv/bin/uv pip install --python .venv/bin/python --no-deps ./tools/parnassus
tools/uv/bin/uv pip check --python .venv/bin/python
python -c "import torch, pythia8mc, pyhepmc, parnassus; print(torch.__version__); print(torch.cuda.is_available()); print(pyhepmc.__version__)"
```

应看到 `2.7.1+cpu`、`False`、pyhepmc 2.16.1 和无依赖冲突。上游源码及许可文件保持完整，版本来源见 [SOURCES](SOURCES.zh-CN.md)。

## 5. 编译必要的 Delphes 目标

ROOT wheel 的 `root-config` 给出的路径带有多余的 `mock_site_packages/ROOT` 段。本项目 `bin/root-config` 只修正该输出，ROOT 安装和 Delphes 源码保持原样。

```bash
cd ~/detector-learning
source env.sh
source .venv/bin/activate
chmod +x bin/root-config
which python
which root-config
root-config --cflags
make -C tools/delphes -j4 RC=root-config libDelphes.so DelphesHepMC3 ClassesDict_rdict.pcm ExRootAnalysisDict_rdict.pcm ModulesDict_rdict.pcm FastJetDict_rdict.pcm
ls -lh tools/delphes/DelphesHepMC3 tools/delphes/libDelphes.so tools/delphes/ClassesDict_rdict.pcm
```

`python` 应位于本项目 `.venv/bin`，`root-config` 应位于本项目 `bin`；头文件路径应指向本项目 ROOT。`-j4` 控制并行编译，不是事件数。只构建必要程序、共享库和字典，避免安装本练习不用的其他读取器或额外 C++ Pythia/HepMC 库。

若此前已经用别处的 ROOT 编译过这个 Delphes，必须先执行 `make -C tools/delphes clean`，再执行上面的构建命令。本机已经完成这次重新编译；普通日常学习无需重复构建。

`env.sh` 提供本项目 ROOT 及其附带库、图形兼容库和 Delphes 头文件的搜索路径，保证生成的字典也能正确加载。

## 6. 校验与开始学习

```bash
cd ~/detector-learning
source env.sh
source .venv/bin/activate
tools/uv/bin/uv pip check --python .venv/bin/python
python -c "import sys, ROOT, pythia8mc, parnassus; print(sys.executable); print(ROOT.__file__); print(pythia8mc.__file__); print(parnassus.__file__); ROOT.gROOT.SetBatch(True); assert ROOT.gSystem.Load('tools/delphes/libDelphes.so') >= 0"
ldd tools/delphes/DelphesHepMC3
```

Python 和导入包的路径应位于 `~/detector-learning`；`ldd` 中 ROOT 库也应来自本项目，其他基础库来自 Linux 系统，不应出现 `~/smeftsim` 或 `not found`。

现在按 [handbook 第 3 节](handbook.zh-CN.md) 手动导出过程、设卡并生成事件。新机器没有本机的参考 LHE，先按手册生成自己的硬事件。MadGraph、Pythia、Parnassus、ROOT 的 Python 操作统一用 `python`。

安装校验不等于物理闭环；事件计数、转换保留、ROOT 分支、图和同种子重放按 handbook 完成。两个项目共享 Linux 系统不影响软件隔离，边界见 [dependencies](dependencies.zh-CN.md)。

大文件只留 Linux：`tools` 是安装工具、解释器和软件源码，`.venv` 是 Python 包环境，`work/dy` 和 `out` 是生成与分析数据。教学文件只附 `examples` 的小图、直方图和验证记录。
