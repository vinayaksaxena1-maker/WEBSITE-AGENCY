import asyncio
from typing import Dict, List, Callable, Any
from core.logger import logger

class WorkflowManager:
    def __init__(self):
        self._workflows: Dict[str, List[str]] = {}
        self._step_handlers: Dict[str, Callable] = {}

    def register_workflow(self, name: str, steps: List[str]) -> None:
        self._workflows[name] = steps
        logger.info(f"Workflow '{name}' registered with steps: {steps}")

    def register_step_handler(self, step_name: str, handler: Callable) -> None:
        self._step_handlers[step_name] = handler
        logger.info(f"Handler for step '{step_name}' registered successfully.")

    async def execute_step(self, step_name: str, context: Any) -> Any:
        if step_name not in self._step_handlers:
            raise ValueError(f"No handler registered for workflow step: {step_name}")
            
        handler = self._step_handlers[step_name]
        logger.info(f"Executing workflow step '{step_name}'...")
        
        if asyncio.iscoroutinefunction(handler):
            return await handler(context)
        else:
            return handler(context)

workflow_manager = WorkflowManager()
