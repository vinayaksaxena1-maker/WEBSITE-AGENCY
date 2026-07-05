import redis.asyncio as aioredis
from config.config import settings
from core.logger import logger
from typing import Optional

class RedisManager:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis_url = redis_url
        self.client = aioredis.from_url(
            self.redis_url, 
            decode_responses=True,
            socket_timeout=5.0
        )

    async def verify_connection(self) -> bool:
        try:
            pong = await self.client.ping()
            if pong:
                logger.info("Redis connection verified successfully.")
                return True
            return False
        except Exception as e:
            logger.error(f"Redis connection verification failed: {e}", exc_info=True)
            return False

    async def push_to_queue(self, queue_name: str, payload: str) -> None:
        try:
            await self.client.rpush(queue_name, payload)
        except Exception as e:
            logger.error(f"Failed to push to Redis queue '{queue_name}': {e}", exc_info=True)
            raise

    async def pop_from_queue(self, queue_name: str) -> Optional[str]:
        try:
            return await self.client.lpop(queue_name)
        except Exception as e:
            logger.error(f"Failed to pop from Redis queue '{queue_name}': {e}", exc_info=True)
            raise

    async def close(self) -> None:
        await self.client.aclose()
        logger.info("Redis connection closed.")

redis_manager = RedisManager()
