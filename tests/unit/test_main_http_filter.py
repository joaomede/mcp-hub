import logging
import pytest

class DummyRecord:
    def __init__(self, path):
        self.path = path
        self.getMessage = lambda: "msg"

from mcp_hub.main import logging as mcp_logging

def test_http_request_filter():
    # Instancia o filtro
    f = None
    for name, obj in mcp_logging.__dict__.items():
        if name == "HTTPRequestFilter":
            f = obj
            break
    assert f is not None
    filt = f()
    # Deve filtrar logs de /health
    rec = DummyRecord("/health")
    assert not filt.filter(rec)
    # Deve aceitar outros
    rec2 = DummyRecord("/foo")
    assert filt.filter(rec2)
