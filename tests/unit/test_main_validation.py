import pytest
from mcp_hub.main import validate_server_config, load_config

# Testa validação de configuração de servidor válida

def test_validate_server_config_valid():
    config = {"command": "echo", "args": ["foo"]}
    validate_server_config("test", config)

# Testa validação de configuração de servidor inválida (sem comando)
def test_validate_server_config_missing_command():
    config = {"args": ["foo"]}
    with pytest.raises(Exception):
        validate_server_config("test", config)

# Testa carregamento e validação de config.json válido
def test_load_config_valid(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text('{"mcpServers": {"srv": {"command": "echo", "args": ["foo"]}}}')
    config = load_config(str(config_path))
    assert "mcpServers" in config
    assert "srv" in config["mcpServers"]

# Testa erro ao carregar config.json inválido
def test_load_config_invalid(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text('{"mcpServers": {"srv": {"args": ["foo"]}}}')
    with pytest.raises(Exception):
        load_config(str(config_path))
