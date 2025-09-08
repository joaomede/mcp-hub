import pytest
import asyncio
import logging
from mcp_hub.utils.config_watcher import ConfigWatcher
import tempfile
import os
import json


def test_config_watcher_invalid_json(monkeypatch, caplog):
    # Cria arquivo temporário com JSON inválido
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("{invalid json}")
        f.flush()
        path = f.name

    called = False
    async def reload_callback(cfg):
        nonlocal called
        called = True

    watcher = ConfigWatcher(path, reload_callback)
    caplog.set_level(logging.ERROR)
    try:
        watcher.start()
        # Força modificação
        os.utime(path, None)
        # Aguarda debounce e processamento
        asyncio.run(asyncio.sleep(1))
    finally:
        watcher.stop()
        os.unlink(path)
    # Deve logar erro de JSON
    assert any("Invalid JSON" in r.message for r in caplog.records)
    assert not called


def test_config_watcher_file_not_found(caplog):
    path = "/tmp/nonexistent_config.json"
    async def reload_callback(cfg):
        pass
    watcher = ConfigWatcher(path, reload_callback)
    caplog.set_level(logging.ERROR)
    watcher.start()
    watcher.stop()
    assert any("does not exist" in r.message for r in caplog.records)


def test_config_watcher_callback_exception(monkeypatch, caplog):
    # Cria arquivo temporário com JSON válido
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        json.dump({"foo": 1}, f)
        f.flush()
        path = f.name

    async def reload_callback(cfg):
        raise RuntimeError("callback error")

    watcher = ConfigWatcher(path, reload_callback)
    caplog.set_level(logging.ERROR)
    try:
        watcher.start()
        os.utime(path, None)
        asyncio.run(asyncio.sleep(1))
    finally:
        watcher.stop()
        os.unlink(path)
    assert any("callback error" in r.message for r in caplog.records)
