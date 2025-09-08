import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mcp_hub.main import mount_config_servers, unmount_servers, validate_server_config, create_sub_app

def make_main_app_with_servers():
    app = FastAPI()
    config_data = {
        "mcpServers": {
            "srv1": {"command": "echo", "args": ["foo"]},
            "srv2": {"command": "echo", "args": ["bar"]}
        }
    }
    mount_config_servers(
        app,
        config_data,
        cors_allow_origins=["*"],
        api_key=None,
        strict_auth=False,
        api_dependency=None,
        connection_timeout=5,
        lifespan=None,
        path_prefix="/"
    )
    return app, config_data

def test_mount_and_unmount_servers():
    app, config_data = make_main_app_with_servers()
    client = TestClient(app)
    # Verifica se as rotas dos servidores estão montadas
    for srv in config_data["mcpServers"]:
        resp = client.post(f"/{srv}/mcp/", json={})
        # Vai retornar 503 pois não há session conectada, mas a rota existe
        assert resp.status_code == 503
    # Unmount srv1
    unmount_servers(app, "/", ["srv1"])
    resp = client.post("/srv1/mcp/", json={})
    assert resp.status_code == 404
    # srv2 ainda existe
    resp = client.post("/srv2/mcp/", json={})
    assert resp.status_code == 503

def test_create_sub_app_with_api_key():
    server_cfg = {"command": "echo", "args": ["foo"]}
    validate_server_config("test", server_cfg)
    app = create_sub_app(
        server_name="test",
        server_cfg=server_cfg,
        cors_allow_origins=["*"],
        api_key="mykey",
        strict_auth=True,
        api_dependency=None,
        connection_timeout=5,
        lifespan=None,
    )
    client = TestClient(app)
    # Sem API key
    resp = client.post("/", json={})
    assert resp.status_code == 401 or resp.status_code == 403
    # Com API key
    resp = client.post("/", json={}, headers={"Authorization": "Bearer mykey"})
    # Vai retornar 503 pois não há session conectada, mas a autenticação passa
    assert resp.status_code == 503
