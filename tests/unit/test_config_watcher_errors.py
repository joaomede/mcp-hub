import pytest
import asyncio
import tempfile
import os
from mcp_hub.utils.config_watcher import ConfigWatcher

# Testa erro de JSON inválido no reload_callback
@pytest.mark.asyncio
async def test_config_watcher_invalid_json(monkeypatch):
    triggered = asyncio.Event()
    async def reload_callback(config):
        triggered.set()
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as tmp:
        tmp.write('{invalid json}')
        tmp.flush()
        watcher = ConfigWatcher(tmp.name, reload_callback)
        watcher.start()
        # Força modificação para disparar reload
        with open(tmp.name, 'w') as f:
            f.write('{invalid json}')
        await asyncio.sleep(0.5)
        watcher.stop()
        os.unlink(tmp.name)
    # Não deve levantar exceção, apenas logar erro
    assert True

# Testa erro de arquivo inexistente
@pytest.mark.asyncio
async def test_config_watcher_file_not_found(monkeypatch):
    async def reload_callback(config):
        pass
    watcher = ConfigWatcher("/tmp/nonexistent_config.json", reload_callback)
    watcher.start()
    # Não deve levantar exceção, apenas logar erro
    watcher.stop()
    assert True
