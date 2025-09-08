
import pytest
from mcp_hub.utils.config_watcher import ConfigWatcher
import tempfile
import os
import time
import asyncio
import threading
import logging

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

    # Testa evento de criação de arquivo
    @pytest.mark.asyncio
    async def test_config_watcher_on_created(monkeypatch):
        triggered = asyncio.Event()
        async def reload_callback(*args, **kwargs):
            triggered.set()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "config.json")
            # Não cria o arquivo ainda
            watcher = ConfigWatcher(path, reload_callback)
            watcher.start()
            await asyncio.sleep(0.2)
            with open(path, 'w') as f:
                f.write('{"created": true}')
            await asyncio.wait_for(triggered.wait(), timeout=2)
            watcher.stop()


    # Testa evento de movimentação de arquivo (rename)
    @pytest.mark.asyncio
    async def test_config_watcher_on_moved(monkeypatch):
        triggered = asyncio.Event()
        async def reload_callback(*args, **kwargs):
            triggered.set()
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "tmp.json")
            dst = os.path.join(tmpdir, "config.json")
            with open(src, 'w') as f:
                f.write('{"foo": 1}')
            watcher = ConfigWatcher(dst, reload_callback)
            watcher.start()
            await asyncio.sleep(0.2)
            os.rename(src, dst)
            await asyncio.wait_for(triggered.wait(), timeout=2)
            watcher.stop()


    # Testa debounce: múltiplas modificações rápidas só disparam um reload
    @pytest.mark.asyncio
    async def test_config_watcher_debounce(monkeypatch):
        count = 0
        event = asyncio.Event()
        async def reload_callback(*args, **kwargs):
            nonlocal count
            count += 1
            event.set()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'{}')
            tmp.flush()
            watcher = ConfigWatcher(tmp.name, reload_callback)
            watcher.start()
            await asyncio.sleep(0.2)
            for _ in range(5):
                with open(tmp.name, 'w') as f:
                    f.write('{"changed": true}')
                await asyncio.sleep(0.1)  # menor que debounce
            await asyncio.wait_for(event.wait(), timeout=2)
            await asyncio.sleep(0.7)  # espera debounce passar
            watcher.stop()
            os.unlink(tmp.name)
        assert count == 1


    # Testa uso em contexto sem event loop (thread própria)
    def test_config_watcher_thread_context():
        triggered = threading.Event()
        def reload_callback(_):
            triggered.set()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'{}')
            tmp.flush()
            watcher = ConfigWatcher(tmp.name, lambda _: asyncio.get_event_loop().call_soon_threadsafe(triggered.set, None))
            watcher.start()
            time.sleep(0.2)
            with open(tmp.name, 'w') as f:
                f.write('{"changed": true}')
            triggered.wait(timeout=2)
            watcher.stop()
            os.unlink(tmp.name)
        assert triggered.is_set()


    # Testa erro inesperado no callback
    @pytest.mark.asyncio
    async def test_config_watcher_callback_exception(monkeypatch, caplog):
        caplog.set_level(logging.ERROR)
        async def reload_callback(_):
            raise RuntimeError("fail reload")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'{}')
            tmp.flush()
            watcher = ConfigWatcher(tmp.name, reload_callback)
            watcher.start()
            await asyncio.sleep(0.2)
            with open(tmp.name, 'w') as f:
                f.write('{"changed": true}')
            await asyncio.sleep(0.5)
            watcher.stop()
            os.unlink(tmp.name)
        assert any("fail reload" in r.message for r in caplog.records)


    # Testa uso do contexto (with ConfigWatcher)
    @pytest.mark.asyncio
    async def test_config_watcher_context_manager(monkeypatch):
        triggered = asyncio.Event()
        async def reload_callback(*args, **kwargs):
            triggered.set()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'{}')
            tmp.flush()
            async with asyncio.Lock():  # Garante que event loop está ativo
                with ConfigWatcher(tmp.name, reload_callback) as watcher:
                    await asyncio.sleep(0.2)
                    with open(tmp.name, 'w') as f:
                        f.write('{"changed": true}')
                    await asyncio.wait_for(triggered.wait(), timeout=2)
            os.unlink(tmp.name)
