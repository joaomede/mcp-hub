import pytest
from fastapi import FastAPI
from mcp_hub.main import reload_config_handler
import asyncio

@pytest.mark.asyncio
async def test_reload_config_handler_partial_changes():
    app = FastAPI()
    app.state.config_data = {"mcpServers": {"srv1": {"command": "echo", "args": ["foo"]}, "srv2": {"command": "echo", "args": ["bar"]}}}
    app.state.cors_allow_origins = ["*"]
    app.state.api_key = None
    app.state.strict_auth = False
    app.state.api_dependency = None
    app.state.connection_timeout = 5
    app.state.lifespan = None
    app.state.path_prefix = "/"
    # Remove srv1, mantém srv2, adiciona srv3
    new_config = {"mcpServers": {"srv2": {"command": "echo", "args": ["bar"]}, "srv3": {"command": "echo", "args": ["baz"]}}}
    await reload_config_handler(app, new_config)
    paths = [str(route.path) for route in app.router.routes if hasattr(route, 'path')]
    assert any("/srv2/mcp" in p for p in paths)
    assert any("/srv3/mcp" in p for p in paths)
    assert not any("/srv1/mcp" in p for p in paths)
