import pytest
from mcp_hub.main import load_config
import tempfile
import os

# Testa load_config com arquivo vazio

def test_load_config_empty_file(tmp_path):
    config_path = tmp_path / "empty.json"
    config_path.write_text("")
    with pytest.raises(Exception):
        load_config(str(config_path))

# Testa load_config com permissão negada (simulado)
def test_load_config_permission_denied(monkeypatch, tmp_path):
    config_path = tmp_path / "denied.json"
    config_path.write_text('{"mcpServers": {}}')
    def raise_permission(*a, **kw):
        raise PermissionError("Permission denied")
    monkeypatch.setattr("builtins.open", lambda *a, **kw: raise_permission())
    with pytest.raises(PermissionError):
        load_config(str(config_path))
