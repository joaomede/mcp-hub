import pytest
from mcp_hub.utils.main import logger

def test_logger_exists():
    assert logger is not None
    assert hasattr(logger, 'info')
    assert hasattr(logger, 'error')
