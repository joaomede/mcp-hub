import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mcp_hub.main import create_sub_app, validate_server_config

def make_test_app():
    server_cfg = {"command": "echo", "args": ["foo"]}
    validate_server_config("test", server_cfg)
    app = create_sub_app(
        server_name="test",
        server_cfg=server_cfg,
        cors_allow_origins=["*"],
        api_key=None,
        strict_auth=False,
        api_dependency=None,
        connection_timeout=5,
        lifespan=None,
    )
    return app

def test_health_check():
    app = FastAPI()
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_sub_app_root_returns_405():
    app = make_test_app()
    client = TestClient(app)
    # O endpoint raiz aceita apenas POST
    resp = client.get("/")
    assert resp.status_code == 405

def test_sub_app_post_missing_session(monkeypatch):
    app = make_test_app()
    client = TestClient(app)
    # Simula ausência de session conectada
    resp = client.post("/", json={"method": "tools/list"})
    assert resp.status_code == 503
    assert "not connected" in resp.json()["detail"]
