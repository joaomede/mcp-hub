import pytest
from mcp_hub.main import validate_server_config

# Testa validação de configuração de servidor
def test_validate_server_config_valid():
    config = {"command": "echo", "args": ["foo"]}
    # Não deve lançar exceção
    validate_server_config("test", config)

def test_validate_server_config_missing_command():
    config = {"args": ["foo"]}
    with pytest.raises(Exception):
        validate_server_config("test", config)
