import pytest
from mcp_hub.utils.auth import create_token, decode_token
from datetime import timedelta
import time

def test_create_and_decode_token():
    data = {"user_id": 123, "role": "admin"}
    token = create_token(data)
    decoded = decode_token(token)
    assert decoded["user_id"] == 123
    assert decoded["role"] == "admin"

def test_create_token_with_expiry():
    data = {"foo": "bar"}
    token = create_token(data, expires_delta=timedelta(seconds=1))
    decoded = decode_token(token)
    assert decoded["foo"] == "bar"
    time.sleep(1.5)
    # Após expirar, decode_token deve retornar None
    assert decode_token(token) is None

def test_decode_token_invalid():
    # Token inválido deve retornar None
    assert decode_token("invalid.token.value") is None
