import pytest
from fastapi.testclient import TestClient
from mcp_hub.main import create_sub_app, validate_server_config

# Testa erro de método desconhecido no proxy MCP
@pytest.mark.asyncio
async def test_proxy_method_not_found():
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
    class FakeSession:
        is_connected = True
        @staticmethod
        async def list_tools():
            return type("FakeToolsResult", (), {"tools": []})()
        @staticmethod
        async def call_tool(name, args=None):
            class FakeResult:
                content = []
            return FakeResult()
        @staticmethod
        async def initialize():
            return None
    app.state.session = FakeSession()
    app.state.is_connected = True
    client = TestClient(app)
    # initialize
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    session_id = resp.json()["result"]["sessionId"]
    # método desconhecido
    resp = client.post("/", json={"jsonrpc": "2.0", "id": 2, "method": "unknown/method"}, headers={"x-session-id": session_id})
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data
    assert data["error"]["code"] == -32601
    assert data["error"]["message"].startswith("Method not found")
