from database.database import db_manager
from database.redis_manager import redis_manager
from core.logger import logger

class HealthMonitor:
    async def check_health(self) -> dict:
        db_ok = await db_manager.verify_connection()
        redis_ok = await redis_manager.verify_connection()
        
        status = {
            "status": "healthy" if (db_ok and redis_ok) else "unhealthy",
            "database": "connected" if db_ok else "disconnected",
            "redis": "connected" if redis_ok else "disconnected"
        }
        
        logger.info(f"System Health Status Checked: {status}")
        return status

health_monitor = HealthMonitor()
