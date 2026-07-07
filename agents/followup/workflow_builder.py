import uuid
from typing import Dict, Any
from agents.followup.followup_contracts import UnifiedInputContract, WorkflowContextContract

class WorkflowBuilder:
    @staticmethod
    def build_context(input_contract: UnifiedInputContract) -> WorkflowContextContract:
        """
        Transforms validated UnifiedInputContract into a unified WorkflowContextContract.
        Applies normalization rules, duplicate resolution, and integrity checks.
        """
        final_email = input_contract.final_email_package
        email_metadata = final_email.metadata
        
        # 1. Normalization: Preserve original identifiers from upstream authoritative source
        email_ref = email_metadata.execution_id
        if not email_ref:
            raise ValueError("Workflow assembly failed: Upstream execution_id is empty.")
            
        # Generate new deterministic or unique workflow and execution IDs
        workflow_id = f"WF-{uuid.uuid4().hex[:12].upper()}"
        execution_ref = f"EX-WF-{uuid.uuid4().hex[:12].upper()}"
        
        # 2. Duplicate Resolution: Consolidate configuration variables safely
        # Ensure that agency config from input overrides email agency config if present
        consolidated_agency_config = {
            **email_metadata.processing_metadata.model_dump(),
            **input_contract.agency_config
        }
        
        # Normalization of field formats and structures
        validation_summary = {
            "validation_id": email_metadata.validation_report.validation_id,
            "validation_status": email_metadata.validation_status,
            "overall_result": email_metadata.validation_report.overall_validation_result,
            "checked_at": email_metadata.validation_report.checked_at,
            "errors": email_metadata.validation_report.errors
        }
        
        processing_summary = {
            "processing_timestamp": email_metadata.processing_metadata.processing_timestamp,
            "processing_status": email_metadata.processing_metadata.processing_status,
            "completion_status": email_metadata.processing_metadata.completion_status,
            "execution_duration_sec": email_metadata.processing_metadata.execution_duration_sec
        }
        
        configuration_summary = {
            "workflow_config": input_contract.workflow_config,
            "followup_config": input_contract.followup_config,
            "agency_config": consolidated_agency_config,
            "brand_voice_config": input_contract.brand_voice_config
        }
        
        # Build Workflow Context and Follow-Up Context
        workflow_context = {
            "workflow_identity": workflow_id,
            "workflow_status": "INITIALIZED",
            "active_step": "WORKFLOW_ASSEMBLY"
        }
        
        followup_context = {
            "recipient_email": final_email.email_payload.target_email,
            "subject": final_email.email_payload.subject,
            "followup_status": "PENDING"
        }
        
        return WorkflowContextContract(
            workflow_id=workflow_id,
            email_ref=email_ref,
            execution_ref=execution_ref,
            validation_summary=validation_summary,
            processing_summary=processing_summary,
            configuration_summary=configuration_summary,
            workflow_context=workflow_context,
            followup_context=followup_context
        )
