import pytest
from mcp_hub.main import validate_server_config

def test_validate_server_config_missing_command():
    with pytest.raises(ValueError, match="must have a 'command' field"):
        validate_server_config("test_server", {})

def test_validate_server_config_invalid_command():
    with pytest.raises(ValueError, match="'command' must be a string"):
        validate_server_config("test_server", {"command": 123})

def test_validate_server_config_invalid_args():
    with pytest.raises(ValueError, match="'args' must be a list"):
        validate_server_config("test_server", {"command": "echo", "args": "not_a_list"})

def test_validate_server_config_valid():
    try:
        validate_server_config("test_server", {"command": "echo", "args": ["hello"]})
    except ValueError:
        pytest.fail("validate_server_config raised ValueError unexpectedly!")
