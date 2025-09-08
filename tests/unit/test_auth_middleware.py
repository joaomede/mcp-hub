import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient
from mcp_hub.utils.auth import APIKeyMiddleware

# Testa autenticação Bearer inválida
def test_apikeymiddleware_invalid_bearer():
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    resp = client.get("/test", headers={"Authorization": "Bearer wrong"})
    assert resp.status_code == 403
    assert resp.json()["detail"] == "Invalid API key"

# Testa autenticação Bearer válida
def test_apikeymiddleware_valid_bearer():
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    resp = client.get("/test", headers={"Authorization": "Bearer mykey"})
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

# Testa autenticação Basic inválida
def test_apikeymiddleware_invalid_basic():
    import base64
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    creds = base64.b64encode(b"user:wrong").decode()
    resp = client.get("/test", headers={"Authorization": f"Basic {creds}"})
    assert resp.status_code == 403
    assert resp.json()["detail"] == "Invalid credentials"

# Testa autenticação Basic válida
def test_apikeymiddleware_valid_basic():
    import base64
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    creds = base64.b64encode(b"user:mykey").decode()
    resp = client.get("/test", headers={"Authorization": f"Basic {creds}"})
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

# Testa método de autenticação não suportado
def test_apikeymiddleware_unsupported_auth():
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    resp = client.get("/test", headers={"Authorization": "Digest something"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Unsupported authorization method"

# Testa ausência de header de autenticação
def test_apikeymiddleware_missing_auth():
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    resp = client.get("/test")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Missing or invalid Authorization header"

# Testa formato inválido de Basic (base64 inválido)
def test_apikeymiddleware_invalid_basic_base64():
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    resp = client.get("/test", headers={"Authorization": "Basic !!!notbase64!!!"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid Basic Authentication format"

# Testa formato inválido de Basic (sem ':')
def test_apikeymiddleware_invalid_basic_no_colon():
    import base64
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key="mykey")
    @app.get("/test")
    async def test():
        return {"ok": True}
    client = TestClient(app)
    creds = base64.b64encode(b"no_colon").decode()
    resp = client.get("/test", headers={"Authorization": f"Basic {creds}"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid Basic Authentication format"

