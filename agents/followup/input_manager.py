from typing import Dict, Any
from agents.followup.followup_contracts import UnifiedInputContract

class InputManager:
    @staticmethod
    def load_inputs(raw_inputs: Dict[str, Any]) -> UnifiedInputContract:
        """
        Loads and validates raw inputs against the UnifiedInputContract schema.
        Ensures that all mandatory upstream information and configurations exist.
        """
        # Ensure that mandatory structures are provided
        if "final_email_package" not in raw_inputs:
            raise ValueError("Input acquisition failed: 'final_email_package' is missing.")
        
        # Verify configs exist (can be empty dictionaries but must be present)
        for config_key in ["followup_config", "workflow_config", "agency_config", "brand_voice_config"]:
            if config_key not in raw_inputs:
                raise ValueError(f"Input acquisition failed: '{config_key}' is missing.")
                
        # Parse and return validated Pydantic model
        try:
            return UnifiedInputContract(**raw_inputs)
        except Exception as e:
            raise ValueError(f"Input validation failed: {e}")
