import pytest
import os
import json
from mcp_hub.main import load_config

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.json")

def test_load_config_invalid_json(tmp_path):
    invalid_json_file = tmp_path / "invalid_config.json"
    invalid_json_file.write_text("{invalid_json}")

    with pytest.raises(json.JSONDecodeError):
        load_config(str(invalid_json_file))

def test_load_config_missing_mcp_servers(tmp_path):
    missing_servers_file = tmp_path / "missing_servers.json"
    missing_servers_file.write_text(json.dumps({}))

    with pytest.raises(ValueError, match="No 'mcpServers' found in config file"):
        load_config(str(missing_servers_file))

def test_load_config_valid(tmp_path):
    valid_config = {
        "mcpServers": {
            "server1": {
                "command": "echo",
                "args": ["hello"]
            }
        }
    }
    valid_config_file = tmp_path / "valid_config.json"
    valid_config_file.write_text(json.dumps(valid_config))

    result = load_config(str(valid_config_file))
    assert result == valid_config
