import pytest
from mcp_hub.main import GracefulShutdown
import asyncio
import signal

# Testa inicialização e sinal de shutdown
def test_graceful_shutdown_sets_event():
    shutdown = GracefulShutdown()
    assert not shutdown.shutdown_event.is_set()
    shutdown.handle_signal(signal.SIGTERM)
    assert shutdown.shutdown_event.is_set()

# Testa rastreamento de tarefas
@pytest.mark.asyncio
async def test_graceful_shutdown_track_task():
    shutdown = GracefulShutdown()
    async def dummy():
        await asyncio.sleep(0.01)
        return 42
    task = asyncio.create_task(dummy())
    shutdown.track_task(task)
    await task
    # Task deve ser removida após conclusão
    assert task not in shutdown.tasks
