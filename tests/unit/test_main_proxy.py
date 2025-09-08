import pytest
from fastapi.testclient import TestClient
from mcp_hub.main import create_sub_app, validate_server_config

# Testa fluxo de sessão: initialize obrigatório antes de tools/list e tools/call
@pytest.mark.asyncio
async def test_proxy_requires_initialize(monkeypatch):
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
    client = TestClient(app)
    # Simula session conectada
    app.state.session = type("FakeSession", (), {
        "list_tools": staticmethod(lambda: ["tool1"]),
        "call_tool": staticmethod(lambda name, args: {"result": 42}),
        "is_connected": True,
        "initialize": staticmethod(lambda: None),
    })()
    app.state.is_connected = True
    # tools/list sem initialize
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert resp.status_code == 200
    assert resp.json()["error"]["message"].startswith("Bad Request: Server not initialized")
    # initialize
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 2, "method": "initialize"})
    assert resp.status_code == 200
    assert "sessionId" in resp.json()["result"]
    # tools/list após initialize
    session_id = resp.json()["result"]["sessionId"]
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 3, "method": "tools/list"}, headers={"x-session-id": session_id})
    assert resp.status_code == 200
    assert "result" in resp.json()
    # tools/call sem initialize (nova sessão)
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "tool1", "arguments": {}}})
    assert resp.status_code == 200
    assert resp.json()["error"]["message"].startswith("Bad Request: Server not initialized")
    # tools/call após initialize
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 5, "method": "initialize"})
    session_id2 = resp.json()["result"]["sessionId"]
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "tool1", "arguments": {}}}, headers={"x-session-id": session_id2})
    assert resp.status_code == 200
    assert "result" in resp.json()
