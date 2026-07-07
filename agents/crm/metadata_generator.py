import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from agents.crm.crm_contracts import MetadataContract, CRMExecutionPackageContract

class MetadataGenerator:
    @staticmethod
    def generate_metadata(formatted: Dict[str, Any]) -> CRMExecutionPackageContract:
        """
        Generates final execution metadata and returns the complete CRMExecutionPackageContract.
        """
        now_str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        execution_id = f"EXEC-CRM-{uuid.uuid4().hex[:12].upper()}"
        
        # Build MetadataContract
        metadata = MetadataContract(
            execution_identifier=execution_id,
            engine_version="CRM-1.0",
            contract_version="1.0",
            processing_timestamp=now_str,
            validation_timestamp=now_str,
            processing_status="COMPLETED",
            validation_status="PASSED",
            execution_metrics={
                "steps_executed": 8,
                "workflow_reference": formatted["formatted_crm_package"]["crm_information"]["workflow_id"]
            }
        )
        
        # Mark publication state as published inside package
        formatted["formatted_crm_package"]["lifecycle_information"]["lifecycle_state"].update({
            "lifecycle_completion_status": "COMPLETED"
        })
        
        return CRMExecutionPackageContract(
            formatted_crm_package=formatted["formatted_crm_package"],
            metadata_package=metadata,
            validation_report=formatted["validation_report"],
            processing_status="COMPLETED"
        )
