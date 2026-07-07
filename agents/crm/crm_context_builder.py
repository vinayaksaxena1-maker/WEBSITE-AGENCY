import uuid
from typing import Dict, Any
from agents.crm.crm_contracts import UnifiedInputContract, CRMContextContract

class CRMContextBuilder:
    @staticmethod
    def build_context(inputs: UnifiedInputContract) -> CRMContextContract:
        """
        Consolidates inputs into a structured and normalized CRMContextContract.
        Resolves duplicate configuration priorities.
        """
        followup_package = inputs.followup_execution_package
        workflow_info = followup_package.formatted_followup_package["workflow_information"]
        workflow_id = workflow_info.get("workflow_id")
        
        if not workflow_id:
            raise ValueError("CRM Context Assembly failed: workflow_id is missing from followup package.")
            
        crm_id = f"CRM-{uuid.uuid4().hex[:12].upper()}"
        
        # Build Customer Context
        customer_context = {
            "customer_id": f"CUST-{uuid.uuid4().hex[:8].upper()}",
            "recipient_email": workflow_info.get("followup_context", {}).get("recipient_email") or workflow_info.get("email_ref"),
            "original_subject": workflow_info.get("followup_context", {}).get("subject") or "Outreach Proposal",
            "relationship_classification": "LEAD",
            "processing_summary": {
                "followup_execution_id": followup_package.metadata_package.execution_id,
                "email_ref": workflow_info.get("email_ref")
            }
        }
        
        # Build Execution Context
        execution_context = {
            "execution_id": followup_package.metadata_package.execution_id,
            "engine_name": "CRM Engine",
            "engine_version": "CRM-1.0",
            "contract_version": "1.0",
            "processing_status": "COMPLETED",
            "validation_status": "PASSED"
        }
        
        # Consolidate config priorities (duplicate resolution)
        consolidated_crm_config = {
            **inputs.workflow_config,
            **inputs.crm_config
        }
        
        crm_context = {
            "crm_identity": crm_id,
            "crm_configuration": consolidated_crm_config,
            "crm_processing_rules": {
                "sync_enabled": consolidated_crm_config.get("sync_enabled", False),
                "auto_promote": consolidated_crm_config.get("auto_promote", True)
            }
        }
        
        lifecycle_context = {
            "lifecycle_stage": "INITIAL",
            "lifecycle_status": "PROSPECT",
            "relationship_state": "ACTIVE"
        }
        
        agency_context = {
            "agency_config": inputs.agency_config,
            "brand_voice_config": inputs.brand_voice_config
        }
        
        return CRMContextContract(
            crm_id=crm_id,
            workflow_id=workflow_id,
            customer_context=customer_context,
            execution_context=execution_context,
            crm_context=crm_context,
            lifecycle_context=lifecycle_context,
            agency_context=agency_context
        )
