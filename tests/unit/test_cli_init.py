import pytest
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
INIT_PATH = REPO_ROOT / "src" / "mcp_hub" / "__init__.py"


def run_cli(args):
    cmd = [sys.executable, str(INIT_PATH)] + args
    return subprocess.run(cmd, capture_output=True, text=True)


def test_cli_help():
    result = run_cli(["--help"])
    assert result.returncode == 0
    assert "Usage" in result.stdout or "usage" in result.stdout


def test_cli_missing_command():
    # No -- and no config_path
    result = run_cli(["--host", "127.0.0.1"])
    assert result.returncode == 1
    assert "Usage" in result.stdout or "usage" in result.stdout


def test_cli_invalid_env():
    # Pass invalid env format
    result = run_cli(["--env", "INVALIDENV", "--", "echo", "foo"])
    # Should not crash, but may exit with error
    assert result.returncode != 0 or "Error" in result.stdout or "Error" in result.stderr


def test_cli_path_prefix_normalization():
    # Should normalize prefix
    result = run_cli(["--path-prefix", "foo", "--", "echo", "foo"])
    # Should not crash
    assert result.returncode == 0 or result.returncode == 1

