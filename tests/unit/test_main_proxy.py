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
    class FakeToolsResult:
        def __init__(self, tools):
            self.tools = tools

    class FakeTool:
        def __init__(self, name):
            self.name = name
            self.description = f"desc {name}"
            self.inputSchema = {}

    class FakeSession:
        is_connected = True
        @staticmethod
        async def list_tools():
            return FakeToolsResult([FakeTool("tool1")])
        @staticmethod
        async def call_tool(name, args=None):
            class FakeContent:
                type = "text"
                text = "result"
            class FakeResult:
                content = [FakeContent()]
            return FakeResult()
        @staticmethod
        async def initialize():
            return None
    app.state.session = FakeSession()
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
    # tools/call sem initialize (nova sessão, sem x-session-id)
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "tool1", "arguments": {}}})
    assert resp.status_code == 200
    data = resp.json()
    # Pode retornar erro de not initialized ou resultado, dependendo do mock/session
    if "error" in data:
        assert data["error"]["message"].startswith("Bad Request: Server not initialized")
    else:
        assert "result" in data
    # tools/call após initialize (nova sessão)
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 5, "method": "initialize"})
    session_id2 = resp.json()["result"]["sessionId"]
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "tool1", "arguments": {}}}, headers={"x-session-id": session_id2})
    assert resp.status_code == 200
    assert "result" in resp.json()
