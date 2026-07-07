from typing import Dict, Any
from agents.email.email_contracts import UnifiedInputPackage

class InputManager:
    @staticmethod
    def load_inputs(raw_inputs: Dict[str, Any]) -> UnifiedInputPackage:
        """
        Loads and validates all mandatory upstream intelligence inputs using Pydantic contracts.
        """
        try:
            return UnifiedInputPackage.model_validate(raw_inputs)
        except Exception as e:
            raise ValueError(f"Mandatory upstream data missing or invalid: {e}")
