import uuid
from datetime import datetime
from agents.followup.followup_contracts import (
    WorkflowContextContract,
    FollowUpSequenceContract,
    FollowUpStateContract,
    ValidatedFollowUpContract
)

class OutputValidator:
    @staticmethod
    def validate_package(
        context: WorkflowContextContract,
        sequence: FollowUpSequenceContract,
        state: FollowUpStateContract
    ) -> ValidatedFollowUpContract:
        """
        Validates all generated Follow-Up components against EDK requirements.
        Generates a Validation Report and returns the ValidatedFollowUpContract.
        """
        errors = []
        
        # 1. Structural/Identity Validation
        if not context.workflow_id:
            errors.append("Missing context.workflow_id")
        if not sequence.sequence_id:
            errors.append("Missing sequence.sequence_id")
        if not sequence.workflow_id or sequence.workflow_id != context.workflow_id:
            errors.append("Sequence workflow_id does not match context workflow_id")
        if not state.workflow_state.get("workflow_id") or state.workflow_state.get("workflow_id") != context.workflow_id:
            errors.append("State workflow_id does not match context workflow_id")
            
        # 2. Sequence Validation
        if not sequence.sequence_stages:
            errors.append("Sequence stages list is empty")
        for stage in sequence.sequence_stages:
            if not stage.get("stage_id") or not stage.get("delay_interval_days"):
                errors.append(f"Invalid sequence stage structure: {stage}")
                
        # 3. State Validation
        if state.workflow_state.get("lifecycle_state") != "ACTIVE":
            errors.append("State lifecycle_state is not ACTIVE")
            
        # Overall result determination
        validation_status = "PASSED" if not errors else "FAILED"
        
        if validation_status == "FAILED":
            raise ValueError(f"Output validation failed: {'; '.join(errors)}")
            
        validation_id = f"VAL-FO-{uuid.uuid4().hex[:12].upper()}"
        
        # Build Approved components
        approved_workflow = context.model_dump()
        approved_sequence = sequence.model_dump()
        
        # Update validation state details in the approved state copy
        approved_state_dict = state.model_dump()
        approved_state_dict["validation_state"].update({
            "validation_status": "COMPLETED",
            "validation_reference": validation_id,
            "validation_lifecycle": "FINAL",
            "validation_result": "VALID"
        })
        
        return ValidatedFollowUpContract(
            approved_workflow=approved_workflow,
            approved_sequence=approved_sequence,
            approved_state=approved_state_dict,
            validation_status=validation_status,
            validation_id=validation_id
        )
