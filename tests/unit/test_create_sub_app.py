import pytest
from fastapi import FastAPI
from mcp_hub.main import create_sub_app

def test_create_sub_app_with_cors():
    server_name = "test_server"
    server_cfg = {"command": "echo", "args": ["hello"]}
    cors_allow_origins = ["http://example.com"]

    app = create_sub_app(
        server_name,
        server_cfg,
        cors_allow_origins,
        api_key=None,
        strict_auth=False,
        api_dependency=None,
        connection_timeout=10,
        lifespan=None,
    )

    assert isinstance(app, FastAPI)
    assert app.title == f"{server_name} MCP Proxy"
    assert app.state.server_type == "stdio"
    assert app.state.command == "echo"
    assert app.state.args == ["hello"]

def test_create_sub_app_with_auth():
    server_name = "test_server"
    server_cfg = {"command": "echo", "args": ["hello"]}
    api_key = "test_key"

    app = create_sub_app(
        server_name,
        server_cfg,
        cors_allow_origins=None,
        api_key=api_key,
        strict_auth=True,
        api_dependency=None,
        connection_timeout=10,
        lifespan=None,
    )

    assert isinstance(app, FastAPI)
    assert app.title == f"{server_name} MCP Proxy"
    assert app.state.server_type == "stdio"
    assert app.state.command == "echo"
    assert app.state.args == ["hello"]
