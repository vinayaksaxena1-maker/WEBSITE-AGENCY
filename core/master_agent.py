import asyncio
from core.logger import logger
from database.redis_manager import redis_manager
from workflows.workflow_manager import workflow_manager

class MasterAgent:
    def __init__(self):
        self.is_running = False
        self.task_queue_name = "agency_tasks"

    async def start(self) -> None:
        self.is_running = True
        logger.info("Master Agent started and listening to tasks queue...")
        asyncio.create_task(self.execution_loop())

    async def stop(self) -> None:
        self.is_running = False
        logger.info("Master Agent shutdown initiated.")

    async def execution_loop(self) -> None:
        while self.is_running:
            try:
                task_payload = await redis_manager.pop_from_queue(self.task_queue_name)
                if task_payload:
                    logger.info(f"Master Agent received task: {task_payload}")
                    await self.process_task(task_payload)
                else:
                    await asyncio.sleep(1.0)
            except Exception as e:
                logger.error(f"Error in Master Agent execution loop: {e}", exc_info=True)
                await asyncio.sleep(5.0)

    async def process_task(self, payload: str) -> None:
        logger.info(f"Successfully processed task payload skeleton: {payload}")

master_agent = MasterAgent()
