#!/bin/bash

set -euo pipefail

VENV_DIR=".venv"
CONDA_FALLBACK_NAME="mcp-hub-py311"

check_py_ge() {
    # Returns 0 if the given command exists and its Python version >= 3.11
    cmd="$1"
    if ! command -v "$cmd" &>/dev/null; then
        return 1
    fi
    "$cmd" -c 'import sys
if sys.version_info >= (3,11):
    sys.exit(0)
else:
    sys.exit(1)
'
}

echo "Locating a Python >= 3.11 to create the venv..."
PYTHON_EXEC=""

if check_py_ge python3.11; then
    PYTHON_EXEC="$(command -v python3.11)"
    echo "Found python3.11 at $PYTHON_EXEC"
fi

if [ -z "$PYTHON_EXEC" ] && check_py_ge python3; then
    PYTHON_EXEC="$(command -v python3)"
    echo "Using python3 at $PYTHON_EXEC"
fi

if [ -z "$PYTHON_EXEC" ] && check_py_ge python; then
    PYTHON_EXEC="$(command -v python)"
    echo "Using python at $PYTHON_EXEC"
fi

if [ -z "$PYTHON_EXEC" ]; then
    if command -v conda &>/dev/null; then
        echo "Python 3.11 not found on PATH. Conda detected. Creating (or reusing) conda env '$CONDA_FALLBACK_NAME' with Python 3.11..."
        if ! conda env list | awk '{print $1}' | grep -q "^$CONDA_FALLBACK_NAME$"; then
            conda create -y -n "$CONDA_FALLBACK_NAME" python=3.11
        fi
        PYTHON_EXEC="$(conda run -n "$CONDA_FALLBACK_NAME" which python)"
        echo "Using Python from conda env: $PYTHON_EXEC"
    else
        echo "No suitable Python (>=3.11) found and conda is not available."
        echo "Please install Python 3.11 or create a conda env with Python 3.11, then re-run this script."
        exit 1
    fi
fi

# Ensure we have an absolute path for python
PYTHON_EXEC="$(readlink -f "$PYTHON_EXEC")"

echo "Creating venv at $VENV_DIR using $PYTHON_EXEC"

# If venv exists but has wrong Python version, recreate it
if [ -d "$VENV_DIR" ]; then
    if [ -x "$VENV_DIR/bin/python" ]; then
        if ! "$VENV_DIR/bin/python" -c 'import sys
sys.exit(0 if sys.version_info >= (3,11) else 1)
'; then
            echo "Existing venv Python is <3.11. Recreating venv..."
            rm -rf "$VENV_DIR"
        else
            echo "Existing venv Python is >=3.11. Keeping venv."
        fi
    else
        echo "Existing venv seems invalid. Recreating..."
        rm -rf "$VENV_DIR"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
fi

# Activate venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Upgrade pip and install editable project + test/dev deps
pip install --upgrade pip
pip install -e .
# Install dev/test deps declared in pyproject and any extras used by tests
pip install -r <(printf "pytest\npytest-asyncio\nrequests\n")

echo "Virtual environment setup complete. Activate it with: source $VENV_DIR/bin/activate"
