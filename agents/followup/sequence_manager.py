import uuid
from typing import List, Dict, Any
from agents.followup.followup_contracts import WorkflowContextContract, FollowUpSequenceContract

class SequenceManager:
    @staticmethod
    def build_sequence(context: WorkflowContextContract) -> FollowUpSequenceContract:
        """
        Transforms validated WorkflowContextContract into a deterministic FollowUpSequenceContract.
        Defines workflow stages (e.g. delay days, retries) based on configuration.
        """
        workflow_id = context.workflow_id
        if not workflow_id:
            raise ValueError("Sequence preparation failed: workflow_id is missing.")
            
        sequence_id = f"SEQ-{uuid.uuid4().hex[:12].upper()}"
        
        # Read follow-up configuration parameters
        followup_config = context.configuration_summary.get("followup_config", {})
        max_retries = followup_config.get("max_retries", 3)
        delay_days = followup_config.get("delay_days", 2)
        
        # Build deterministic stages
        stages = []
        for i in range(1, max_retries + 1):
            stages.append({
                "stage_number": i,
                "stage_id": f"STAGE-{sequence_id}-{i}",
                "delay_interval_days": delay_days * i,
                "description": f"Follow-up attempt #{i} after {delay_days * i} days.",
                "action": "SEND_EMAIL_FOLLOWUP",
                "status": "PENDING"
            })
            
        sequence_definition = {
            "name": f"Follow-Up Sequence for Workflow {workflow_id}",
            "type": "EMAIL_SEQUENCE",
            "total_stages": len(stages)
        }
        
        sequence_metadata = {
            "sequence_version": "1.0",
            "schema_version": "1.0.0"
        }
        
        processing_context = {
            "recipient_email": context.followup_context.get("recipient_email"),
            "original_subject": context.followup_context.get("subject")
        }
        
        return FollowUpSequenceContract(
            sequence_id=sequence_id,
            workflow_id=workflow_id,
            sequence_definition=sequence_definition,
            sequence_stages=stages,
            sequence_metadata=sequence_metadata,
            processing_context=processing_context
        )
