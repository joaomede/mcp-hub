
import pytest
from mcp_hub.utils.config_watcher import ConfigWatcher
import tempfile
import os
import time
import asyncio

# Testa se o watcher detecta modificação em arquivo
@pytest.mark.asyncio
async def test_config_watcher_triggers_reload(monkeypatch):
    triggered = asyncio.Event()
    async def reload_callback(*args, **kwargs):
        triggered.set()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b'{}')
        tmp.flush()
        watcher = ConfigWatcher(tmp.name, reload_callback)
        watcher.start()
        await asyncio.sleep(0.2)
        with open(tmp.name, 'w') as f:
            f.write('{"changed": true}')
        await asyncio.wait_for(triggered.wait(), timeout=2)
        watcher.stop()
        os.unlink(tmp.name)
