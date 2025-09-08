import pytest
from mcp_hub.main import GracefulShutdown
import asyncio
import signal

# Testa handle_signal com sinal inesperado

def test_graceful_shutdown_unexpected_signal():
    shutdown = GracefulShutdown()
    # Sinal não padrão (ex: SIGUSR1)
    shutdown.handle_signal(signal.SIGUSR1)
    assert shutdown.shutdown_event.is_set()

# Testa track_task com task já finalizada
@pytest.mark.asyncio
async def test_graceful_shutdown_track_task_done():
    shutdown = GracefulShutdown()
    async def dummy():
        return 42
    task = asyncio.create_task(dummy())
    await task
    shutdown.track_task(task)
    # Task já finalizada deve ser removida imediatamente
    assert task not in shutdown.tasks
