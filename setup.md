# Standalone Linux setup and rebuilding

[简体中文](setup.zh-CN.md)

The prepared machine has already passed installation and runtime checks: use the [handbook](handbook.md). This page is for a new machine or a rebuild. **You do not need to install the SMEFTsim tutorial first.** See [dependencies.md](dependencies.md) for the dependency layers.

The pinned route uses x86-64 Ubuntu 22.04, project-local Python 3.12.12, one `.venv`, and the project's own MadGraph, ROOT, Pythia, Delphes and Parnassus. Linux supplies the compilers; Python and scientific software live inside the project. These steps do not change Windows Python or another project's environment.

Enter each complete Bash command, press Enter once, and wait for the prompt before the next command. Only commands marked PowerShell run in Windows. Edit card contents in an editor. If a directory or environment already exists, check its version and skip creation rather than overwriting it.

## 1. Prepare Linux

The prepared machine can keep using its WSL distribution named `SMEFTsim`; a second virtual disk is unnecessary.

On a new Windows machine, follow [Microsoft's WSL installation guide](https://learn.microsoft.com/windows/wsl/install) to install Ubuntu 22.04. In an administrator **PowerShell** window:

```powershell
wsl --install -d Ubuntu-22.04
```

Restart if prompted, launch Ubuntu, and choose your Linux username and password. All commands below run in **Linux Bash**. Skip this paragraph if you already use native Ubuntu or WSL Ubuntu.

Install the system tools once:

```bash
sudo apt-get update
sudo apt-get install -y build-essential gfortran git curl ca-certificates perl nano
uname -m
g++ --version
gfortran --version
```

Expect `x86_64` and compiler version information. Here `sudo` installs Linux system tools, never Python packages. The prepared machine already has these tools.

## 2. Obtain the teaching files

Clone inside the Linux filesystem, rather than `/mnt/c`:

```bash
git clone https://github.com/RuneTan/detector-learning.git ~/detector-learning
cd ~/detector-learning
mkdir -p tools work out
source env.sh
```

If the repository is already present, skip cloning and enter its directory. `env.sh` finds the project from its own location and keeps Python downloads, the uv cache and terminal paths inside it; it does not edit `.bashrc`. Python and ROOT will be created below.

Windows File Explorer can access the project at `\\wsl.localhost\YOUR-DISTRIBUTION\home\YOUR-USERNAME\detector-learning`. The prepared machine uses `\\wsl.localhost\SMEFTsim\home\smeft\detector-learning`.

`enter-linux.ps1` contains that machine's distribution, username and Linux directory. Replace them before using the launcher elsewhere. Native Linux does not need Windows launchers.

## 3. Install project-local Python and scientific packages

Download the standalone executable from the [pinned uv release](https://github.com/astral-sh/uv/releases/tag/0.9.28) and extract it inside the project, without using another project's pip:

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

Expect uv 0.9.28 and Python 3.12.12. The base interpreter lives in `tools/python`, and third-party packages in `.venv`; both form the project's Python runtime. Do not move or copy `.venv` alone. Rebuild using this page when changing directories or machines.

This exercise uses CPU PyTorch. Install its CPU wheel first, followed by the locked dependencies, which include the CPython 3.12 ROOT wheel:

```bash
tools/uv/bin/uv pip install --python .venv/bin/python torch==2.7.1+cpu --index-url https://download.pytorch.org/whl/cpu
tools/uv/bin/uv pip install --python .venv/bin/python -r requirements.lock.txt
```

The lock file records runtime dependencies. Install Parnassus itself from pinned source in the next section. Do not run `uv sync --all-extras`: this exercise needs no development extras, CUDA packages or neural-model training tools.

ROOT wheel `0.1a12` contains ROOT 6.40.00. This is the pinned, tested build for the tutorial, not a claim about the latest release. It provides C++ ROOT libraries, command-line tools and PyROOT. A wheel for a different Python minor version cannot be reused.

The prepared minimal Ubuntu lacks libSM/libICE required by ROOT graphics. Download Ubuntu packages and **extract them inside the project**, without installing them with `sudo`:

```bash
mkdir -p .venv/local-libs/debs
cd .venv/local-libs/debs
apt-get download libsm6 libice6
```

The next block is a Bash loop. After the first line the shell shows a continuation prompt. The two spaces on the second line are for readability. Pressing Enter after `done` executes it; no additional blank line is needed:

```bash
for archive in *.deb; do
  dpkg-deb -x "$archive" ..
done
```

Return to the project root:

```bash
cd ../../..
source env.sh
python -c "import ROOT, torch; print(ROOT.gROOT.GetVersion()); print(torch.__version__)"
```

Expect ROOT 6.40.00 and PyTorch 2.7.1+cpu. ROOT may warn that the wheel is an alpha release; the tutorial uses the small configuration tested here.

## 4. Download independent upstream source trees

If the target directories already exist, skip cloning and check their versions. These commands download from upstream rather than copying or borrowing files from `~/smeftsim`:

```bash
git clone --branch v2.9.27 --depth 1 https://github.com/mg5amcnlo/mg5amcnlo.git tools/mg
git clone --branch 3.5.1 --depth 1 https://github.com/delphes/delphes.git tools/delphes
git clone https://github.com/parnassus-hep/parnassus.git tools/parnassus
git -C tools/parnassus checkout c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865
git -C tools/mg rev-parse HEAD
git -C tools/delphes rev-parse HEAD
git -C tools/parnassus rev-parse HEAD
```

The commits should be:

- MadGraph: `eb76cab72b8d44aac7162ac7221ac08a4384a169`.
- Delphes: `28658365abeb71ee36dfc739f9670c1514c0cb10`.
- Parnassus: `c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865`.

Install Parnassus without resolving or upgrading the dependencies already installed from the lock file:

```bash
tools/uv/bin/uv pip install --python .venv/bin/python --no-deps ./tools/parnassus
tools/uv/bin/uv pip check --python .venv/bin/python
python -c "import torch, pythia8mc, pyhepmc, parnassus; print(torch.__version__); print(torch.cuda.is_available()); print(pyhepmc.__version__)"
```

Expect `2.7.1+cpu`, `False`, pyhepmc 2.16.1, and no dependency conflicts. Keep upstream source and license files intact; [SOURCES.md](SOURCES.md) records their provenance.

## 5. Build the necessary Delphes targets

The pinned ROOT wheel's `root-config` output contains an extra `mock_site_packages/ROOT` path segment. This project's `bin/root-config` corrects only that output, leaving ROOT and Delphes source unchanged.

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

`python` should be in this project's `.venv/bin`; `root-config` in its `bin`. Header paths should point to its ROOT installation. `-j4` controls parallel compilation, not event count. Build only the required program, shared library and dictionaries; this exercise needs no additional readers or C++ Pythia/HepMC libraries.

If this Delphes tree was previously built against another ROOT installation, first run `make -C tools/delphes clean`, then build as above. The prepared machine has already been rebuilt; daily use does not require recompilation.

`env.sh` supplies search paths for this project's ROOT, bundled libraries, graphics compatibility libraries and Delphes headers, allowing the generated dictionaries to load correctly.

## 6. Validate and start learning

```bash
cd ~/detector-learning
source env.sh
source .venv/bin/activate
tools/uv/bin/uv pip check --python .venv/bin/python
python -c "import sys, ROOT, pythia8mc, parnassus; print(sys.executable); print(ROOT.__file__); print(pythia8mc.__file__); print(parnassus.__file__); ROOT.gROOT.SetBatch(True); assert ROOT.gSystem.Load('tools/delphes/libDelphes.so') >= 0"
ldd tools/delphes/DelphesHepMC3
```

Python and imported package paths should be inside `~/detector-learning`. ROOT libraries in `ldd` should also come from this project; basic libraries come from Linux. There should be no `~/smeftsim` paths or `not found` entries.

Continue with [handbook section 3](handbook.md): manually export the process, configure cards and generate events. A new machine has no full reference LHE, so generate your own hard events first. Use the same `python` for MadGraph, Pythia, Parnassus and ROOT.

An installation check is not physics closure. Follow the handbook for event counts, conversion preservation, ROOT branches, plots and same-seed replay. Sharing a Linux system does not break software isolation; see [dependencies.md](dependencies.md).

Keep large files in Linux: `tools` holds installation tools, the interpreter and software sources; `.venv` holds Python packages; `work/dy` and `out` hold generated code and simulation data. Only the small `examples` figures, histograms and validation records accompany the tutorial.
