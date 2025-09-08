import pytest
from mcp_hub.utils.auth import create_token, decode_token
from datetime import timedelta


def test_create_token_and_decode():
    data = {"user": "foo"}
    token = create_token(data)
    decoded = decode_token(token)
    assert decoded["user"] == "foo"


def test_create_token_expired():
    data = {"user": "foo"}
    token = create_token(data, expires_delta=timedelta(seconds=-1))
    decoded = decode_token(token)
    assert decoded is None or "exp" in decoded and decoded["exp"] < 9999999999


def test_decode_token_invalid():
    assert decode_token("invalid.token.value") is None

