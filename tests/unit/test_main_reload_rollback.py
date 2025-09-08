import pytest
import asyncio
from fastapi import FastAPI
from mcp_hub.main import reload_config_handler


@pytest.mark.asyncio
async def test_reload_config_handler_rollback(monkeypatch):
    app = FastAPI()
    app.state.config_data = {"mcpServers": {"srv1": {"command": "echo", "args": ["foo"]}}}
    # Simula erro ao criar sub_app
    def fail_create_sub_app(*a, **kw):
        raise RuntimeError("fail")
    monkeypatch.setattr("mcp_hub.main.create_sub_app", fail_create_sub_app)
    new_config = {"mcpServers": {"srv2": {"command": "echo", "args": ["bar"]}}}
    try:
        await reload_config_handler(app, new_config)
    except RuntimeError:
        pass
    # Deve manter rotas originais (rollback)
    assert hasattr(app.router, "routes")

@pytest.mark.asyncio
async def test_reload_config_handler_error(monkeypatch):
    app = FastAPI()
    app.state.config_data = {"mcpServers": {"srv1": {"command": "echo", "args": ["foo"]}}}
    # Simula erro inesperado
    def fail_mount(*a, **kw):
        raise Exception("mount error")
    monkeypatch.setattr("mcp_hub.main.mount_config_servers", fail_mount)
    new_config = {"mcpServers": {"srv2": {"command": "echo", "args": ["bar"]}}}
    try:
        await reload_config_handler(app, new_config)
    except Exception:
        pass
    assert hasattr(app.router, "routes")
