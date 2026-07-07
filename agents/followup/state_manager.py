from datetime import datetime, timezone
from agents.followup.followup_contracts import FollowUpSequenceContract, FollowUpStateContract

class StateManager:
    @staticmethod
    def initialize_state(sequence: FollowUpSequenceContract) -> FollowUpStateContract:
        """
        Initializes and returns the FollowUpStateContract from a prepared sequence.
        """
        workflow_id = sequence.workflow_id
        if not workflow_id:
            raise ValueError("State initialization failed: workflow_id is missing.")
            
        workflow_state = {
            "workflow_id": workflow_id,
            "current_status": "INITIALIZED",
            "lifecycle_state": "ACTIVE",
            "completion_status": "PENDING"
        }
        
        processing_state = {
            "processing_id": f"PROC-{sequence.sequence_id}",
            "processing_status": "INITIALIZED",
            "processing_stage": "STATE_INITIALIZATION",
            "processing_result": "SUCCESS"
        }
        
        validation_state = {
            "validation_status": "NOT_STARTED",
            "validation_reference": "",
            "validation_lifecycle": "INITIAL",
            "validation_result": ""
        }
        
        publication_state = {
            "publication_status": "UNPUBLISHED",
            "publication_readiness": "NOT_READY",
            "publication_lifecycle": "INITIAL",
            "publication_result": ""
        }
        
        state_metadata = {
            "state_version": "1.0",
            "schema_version": "1.0.0",
            "state_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
        
        return FollowUpStateContract(
            workflow_state=workflow_state,
            processing_state=processing_state,
            validation_state=validation_state,
            publication_state=publication_state,
            state_metadata=state_metadata
        )
