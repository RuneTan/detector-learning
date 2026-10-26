# Source from any Linux Bash terminal; changes apply to this terminal only.
export DETECTOR_HOME="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export DETECTOR_ROOT="$DETECTOR_HOME/.venv/lib/python3.12/site-packages/ROOT"
export PATH="$DETECTOR_HOME/.venv/bin:$DETECTOR_HOME/bin:$DETECTOR_ROOT/bin:$PATH"
export LD_LIBRARY_PATH="$DETECTOR_HOME/tools/delphes:$DETECTOR_ROOT/lib:$DETECTOR_ROOT/../root.libs:$DETECTOR_HOME/.venv/local-libs/usr/lib/x86_64-linux-gnu"
export ROOT_INCLUDE_PATH="$DETECTOR_HOME/tools/delphes:$DETECTOR_HOME/tools/delphes/external"
export UV_CACHE_DIR="$DETECTOR_HOME/tools/cache"
export UV_PYTHON_INSTALL_DIR="$DETECTOR_HOME/tools/python"
export UV_PYTHON_BIN_DIR="$DETECTOR_HOME/tools/bin"
