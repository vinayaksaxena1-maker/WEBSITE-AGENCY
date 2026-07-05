from typing import Dict, Any
from core.logger import logger

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, Any] = {}

    def register_agent(self, name: str, agent_instance: Any) -> None:
        self._agents[name] = agent_instance
        logger.info(f"Agent '{name}' successfully registered in system registry.")

    def get_agent(self, name: str) -> Any:
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not found in registry.")
        return self._agents[name]

    def list_agents(self) -> list:
        return list(self._agents.keys())

agent_registry = AgentRegistry()
