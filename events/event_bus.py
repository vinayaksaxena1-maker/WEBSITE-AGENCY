import asyncio
from typing import Callable, Dict, List, Any
from core.logger import logger

class EventBus:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(handler)
        logger.info(f"Subscribed handler '{handler.__name__}' to event type '{event_type}'.")

    async def publish(self, event_type: str, data: Any) -> None:
        if event_type not in self._listeners:
            return
        
        logger.debug(f"Publishing event '{event_type}' with data: {data}")
        tasks = []
        for handler in self._listeners[event_type]:
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(data))
            else:
                try:
                    handler(data)
                except Exception as e:
                    logger.error(f"Error in sync handler for event '{event_type}': {e}", exc_info=True)
                    
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    logger.error(f"Error in async handler for event '{event_type}': {res}", exc_info=res)

event_bus = EventBus()
