import pytest
import logging
from mcp_hub.main import GracefulShutdown
import asyncio


def test_graceful_shutdown_track_task_done():
    shutdown = GracefulShutdown()
    async def dummy():
        return 42
    task = asyncio.create_task(dummy())
    asyncio.get_event_loop().run_until_complete(task)
    shutdown.track_task(task)
    # Task já finalizada deve ser removida imediatamente
    assert task not in shutdown.tasks


def test_graceful_shutdown_handle_signal_sets_event():
    shutdown = GracefulShutdown()
    shutdown.handle_signal(2)  # SIGINT
    assert shutdown.shutdown_event.is_set()

