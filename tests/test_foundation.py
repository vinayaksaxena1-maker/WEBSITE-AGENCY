import pytest
import asyncio
from config.config import settings
from core.logger import logger, correlation_id_ctx
from events.event_bus import event_bus
from workflows.workflow_manager import workflow_manager
from core.agent_registry import agent_registry

def test_settings_load():
    assert settings.ENVIRONMENT in ["development", "production", "testing"]
    assert settings.LOG_LEVEL in ["INFO", "DEBUG", "WARNING", "ERROR"]

def test_logger_correlation_id():
    correlation_id_ctx.set("TEST-ID-123")
    logger.info("Test logging message")
    assert correlation_id_ctx.get() == "TEST-ID-123"

@pytest.mark.asyncio
async def test_event_bus():
    received = []
    async def async_handler(data):
        received.append(data)
    
    event_bus.subscribe("test_event", async_handler)
    await event_bus.publish("test_event", {"payload": "data"})
    assert len(received) == 1
    assert received[0]["payload"] == "data"

def test_workflow_manager():
    workflow_manager.register_workflow("outdate_check", ["search", "audit"])
    assert "outdate_check" in workflow_manager._workflows
    assert workflow_manager._workflows["outdate_check"] == ["search", "audit"]

def test_agent_registry():
    class DummyAgent:
        pass
    agent = DummyAgent()
    agent_registry.register_agent("dummy", agent)
    assert agent_registry.get_agent("dummy") == agent
