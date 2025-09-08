import pytest
from mcp_hub.main import validate_server_config, load_config, reload_config_handler
from fastapi import FastAPI
import asyncio

# Testa erro de configuração inválida (sem mcpServers)
def test_load_config_no_mcpservers(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text('{"foo": 123}')
    with pytest.raises(ValueError):
        load_config(str(config_path))

# Testa erro de arquivo inexistente
def test_load_config_file_not_found(tmp_path):
    config_path = tmp_path / "notfound.json"
    with pytest.raises(FileNotFoundError):
        load_config(str(config_path))

# Testa erro de JSON inválido
def test_load_config_invalid_json(tmp_path):
    config_path = tmp_path / "bad.json"
    config_path.write_text('{invalid json}')
    with pytest.raises(Exception):
        load_config(str(config_path))

# Testa reload_config_handler com config sem mudanças
@pytest.mark.asyncio
async def test_reload_config_handler_no_change():
    app = FastAPI()
    app.state.config_data = {"mcpServers": {"srv": {"command": "echo", "args": ["foo"]}}}
    app.state.cors_allow_origins = ["*"]
    app.state.api_key = None
    app.state.strict_auth = False
    app.state.api_dependency = None
    app.state.connection_timeout = 5
    app.state.lifespan = None
    app.state.path_prefix = "/"
    # Nenhuma mudança
    await reload_config_handler(app, app.state.config_data)

# Testa reload_config_handler com adição e remoção de servidor
@pytest.mark.asyncio
async def test_reload_config_handler_add_remove():
    app = FastAPI()
    app.state.config_data = {"mcpServers": {"srv1": {"command": "echo", "args": ["foo"]}}}
    app.state.cors_allow_origins = ["*"]
    app.state.api_key = None
    app.state.strict_auth = False
    app.state.api_dependency = None
    app.state.connection_timeout = 5
    app.state.lifespan = None
    app.state.path_prefix = "/"
    new_config = {"mcpServers": {"srv2": {"command": "echo", "args": ["bar"]}}}
    await reload_config_handler(app, new_config)
    # Após reload, srv2 deve estar montado
    found = any("/srv2/mcp" in str(route.path) for route in app.router.routes if hasattr(route, 'path'))
    assert found
