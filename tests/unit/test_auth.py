
import pytest
from mcp_hub.utils.auth import get_verify_api_key, APIKeyMiddleware
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials


# Testa se o verificador de API key rejeita chave inválida
@pytest.mark.asyncio
async def test_verify_api_key_invalid():
    verify = get_verify_api_key("valid-key")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid-key")
    with pytest.raises(HTTPException):
        await verify(credentials)

# Testa se o verificador de API key aceita chave válida
@pytest.mark.asyncio
async def test_verify_api_key_valid():
    verify = get_verify_api_key("valid-key")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid-key")
    # Não deve lançar exceção
    await verify(credentials)
