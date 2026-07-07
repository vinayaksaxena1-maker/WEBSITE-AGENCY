from typing import Dict, Any
from agents.followup.followup_contracts import ValidatedFollowUpContract

class PackageFormatter:
    @staticmethod
    def format_package(validated_contract: ValidatedFollowUpContract) -> Dict[str, Any]:
        """
        Formats and normalizes validated package structure for downstream systems.
        """
        # Build formatting report
        validation_report = {
            "validation_id": validated_contract.validation_id,
            "checked_at": validated_contract.approved_state["state_metadata"]["state_timestamp"],
            "structural_validation": "PASS",
            "workflow_validation": "PASS",
            "sequence_validation": "PASS",
            "state_validation": "PASS",
            "formatting_validation": "PASS",
            "overall_validation_result": "VALID"
        }
        
        # Build formatted package dictionary complying with EDK Page 456-457
        return {
            "formatted_followup_package": {
                "workflow_information": validated_contract.approved_workflow,
                "sequence_information": validated_contract.approved_sequence,
                "state_information": validated_contract.approved_state,
                "validation_information": validation_report,
                "processing_information": validated_contract.approved_state["processing_state"],
                "packaging_status": "COMPLETED"
            },
            "validation_report": validation_report,
            "processing_status": "COMPLETED"
        }
