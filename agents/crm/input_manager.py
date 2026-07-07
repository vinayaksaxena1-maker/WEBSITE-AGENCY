from typing import Dict, Any
from agents.crm.crm_contracts import UnifiedInputContract

class InputManager:
    @staticmethod
    def load_inputs(raw_inputs: Dict[str, Any]) -> UnifiedInputContract:
        """
        Validates raw dictionary inputs against the UnifiedInputContract schema.
        """
        try:
            return UnifiedInputContract(**raw_inputs)
        except Exception as e:
            raise ValueError(f"CRM Input acquisition failed: {e}")
