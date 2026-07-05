from core.logger import logger
from core.health_monitor import health_monitor

class Dashboard:
    async def render(self) -> None:
        logger.info("=== CLI Admin Dashboard Status ===")
        status = await health_monitor.check_health()
        logger.info(f"System State: {status['status'].upper()}")
        logger.info(f"Database Pool: {status['database'].upper()}")
        logger.info(f"Redis Connection: {status['redis'].upper()}")
        logger.info("==================================")

dashboard = Dashboard()
