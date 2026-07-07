import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from agents.followup.followup_contracts import MetadataContract, FollowUpExecutionPackageContract

class MetadataGenerator:
    @staticmethod
    def generate_metadata(formatted_dict: Dict[str, Any]) -> FollowUpExecutionPackageContract:
        """
        Generates final execution metadata and returns the complete FollowUpExecutionPackageContract.
        """
        now_str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        execution_id = f"EXEC-FO-{uuid.uuid4().hex[:12].upper()}"
        
        # Build MetadataContract
        metadata = MetadataContract(
            execution_id=execution_id,
            engine_version="FOLLOWUP-1.0",
            contract_version="1.0",
            processing_timestamp=now_str,
            validation_timestamp=now_str,
            processing_status="COMPLETED",
            validation_status="PASSED",
            execution_metrics={
                "steps_executed": 7,
                "stages_generated": len(formatted_dict["formatted_followup_package"]["sequence_information"]["sequence_stages"])
            }
        )
        
        # Mark publication state as published inside package
        formatted_dict["formatted_followup_package"]["state_information"]["publication_state"].update({
            "publication_status": "PUBLISHED",
            "publication_readiness": "READY",
            "publication_lifecycle": "FINAL",
            "publication_result": "SUCCESS"
        })
        
        # Assemble FollowUpExecutionPackageContract
        return FollowUpExecutionPackageContract(
            formatted_followup_package=formatted_dict["formatted_followup_package"],
            metadata_package=metadata,
            validation_report=formatted_dict["validation_report"],
            processing_status="COMPLETED"
        )
