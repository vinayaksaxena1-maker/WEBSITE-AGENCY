import asyncio
from typing import Callable, Dict
from core.logger import logger
from datetime import datetime, timezone

class Scheduler:
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.is_running = False

    async def start(self) -> None:
        self.is_running = True
        logger.info("Scheduler started.")

    async def schedule_cron(self, name: str, interval_seconds: float, job: Callable, *args, **kwargs) -> None:
        if name in self.tasks:
            raise ValueError(f"Task with name '{name}' already scheduled.")
            
        async def loop_job():
            while self.is_running:
                try:
                    logger.debug(f"Scheduler invoking job '{name}' at {datetime.now(timezone.utc).isoformat()}")
                    if asyncio.iscoroutinefunction(job):
                        await job(*args, **kwargs)
                    else:
                        job(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in scheduler job '{name}': {e}", exc_info=True)
                await asyncio.sleep(interval_seconds)

        self.tasks[name] = asyncio.create_task(loop_job())
        logger.info(f"Cron task '{name}' scheduled with interval {interval_seconds}s.")

    async def cancel_task(self, name: str) -> None:
        if name in self.tasks:
            self.tasks[name].cancel()
            del self.tasks[name]
            logger.info(f"Scheduled task '{name}' cancelled.")

    async def stop(self) -> None:
        self.is_running = False
        for name, task in list(self.tasks.items()):
            task.cancel()
        self.tasks.clear()
        logger.info("Scheduler stopped.")

scheduler = Scheduler()
