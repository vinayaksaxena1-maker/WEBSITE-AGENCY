import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from config.config import settings
from events.event_bus import EventBus
from database.redis_manager import RedisManager

def test_settings_integrity():
    assert settings.DATABASE_URL is not None
    assert settings.REDIS_URL is not None

@pytest.mark.asyncio
async def test_event_bus_publishing():
    bus = EventBus()
    calls = []
    
    async def sample_handler(data):
        calls.append(data)
        
    bus.subscribe("my_test_type", sample_handler)
    await bus.publish("my_test_type", {"test": "data"})
    
    assert len(calls) == 1
    assert calls[0]["test"] == "data"

@pytest.mark.asyncio
async def test_redis_manager_mock():
    # Mocking redis client for list operations tests
    mock_client = AsyncMock()
    mock_client.ping.return_value = "PONG"
    mock_client.rpush.return_value = 1
    mock_client.lpop.return_value = "my-payload"
    
    with patch("redis.asyncio.from_url", return_value=mock_client):
        mgr = RedisManager("redis://localhost:6379")
        
        verified = await mgr.verify_connection()
        assert verified is True
        
        await mgr.push_to_queue("q1", "p1")
        mock_client.rpush.assert_called_once_with("q1", "p1")
        
        res = await mgr.pop_from_queue("q1")
        assert res == "my-payload"
        mock_client.lpop.assert_called_once_with("q1")
        
        await mgr.close()
        mock_client.aclose.assert_called_once()
