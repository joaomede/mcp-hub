import pytest
from mcp_hub.main import validate_server_config

# Testa validação de configuração com tipos errados
@pytest.mark.parametrize("server_cfg", [
    None,
    123,
    "string",
    [],
    {"command": 123, "args": "notalist"},
    {"command": None, "args": None},
    {"command": "", "args": []},
])
def test_validate_server_config_invalid_types(server_cfg):
    with pytest.raises(Exception):
        validate_server_config("test", server_cfg)
