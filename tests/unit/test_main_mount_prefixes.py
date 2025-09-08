import pytest
from fastapi import FastAPI
from mcp_hub.main import mount_config_servers, unmount_servers

def test_mount_unmount_multiple_prefixes():
    app = FastAPI()
    config1 = {"mcpServers": {"srvA": {"command": "echo", "args": ["a"]}}}
    config2 = {"mcpServers": {"srvB": {"command": "echo", "args": ["b"]}}}
    # Monta dois prefixos diferentes
    mount_config_servers(app, config1, cors_allow_origins=["*"], api_key=None, strict_auth=False, api_dependency=None, connection_timeout=5, lifespan=None, path_prefix="/foo/")
    mount_config_servers(app, config2, cors_allow_origins=["*"], api_key=None, strict_auth=False, api_dependency=None, connection_timeout=5, lifespan=None, path_prefix="/bar/")
    # Unmount apenas um prefixo
    unmount_servers(app, "/foo/", ["srvA"])
    # srvA removido, srvB permanece
    paths = [str(route.path) for route in app.router.routes if hasattr(route, 'path')]
    assert any("/bar/srvB/mcp" in p for p in paths)
    assert not any("/foo/srvA/mcp" in p for p in paths)
