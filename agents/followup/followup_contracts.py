from pydantic import BaseModel, Field
from typing import Dict, Any, List
from agents.email.email_contracts import FinalEmailPackage

class UnifiedInputContract(BaseModel):
    final_email_package: FinalEmailPackage
    followup_config: Dict[str, Any] = Field(default_factory=dict)
    workflow_config: Dict[str, Any] = Field(default_factory=dict)
    agency_config: Dict[str, Any] = Field(default_factory=dict)
    brand_voice_config: Dict[str, Any] = Field(default_factory=dict)

class WorkflowContextContract(BaseModel):
    workflow_id: str
    email_ref: str
    execution_ref: str
    validation_summary: Dict[str, Any]
    processing_summary: Dict[str, Any]
    configuration_summary: Dict[str, Any]
    workflow_context: Dict[str, Any]
    followup_context: Dict[str, Any]

# Placeholder contracts for downstream Phase 9 layers (9.6+)
class FollowUpSequenceContract(BaseModel):
    sequence_id: str
    workflow_id: str
    sequence_definition: Dict[str, Any]
    sequence_stages: List[Dict[str, Any]] = Field(default_factory=list)
    sequence_metadata: Dict[str, Any] = Field(default_factory=dict)
    processing_context: Dict[str, Any] = Field(default_factory=dict)

class FollowUpStateContract(BaseModel):
    workflow_state: Dict[str, Any]
    processing_state: Dict[str, Any]
    validation_state: Dict[str, Any]
    publication_state: Dict[str, Any]
    state_metadata: Dict[str, Any] = Field(default_factory=dict)

class ValidatedFollowUpContract(BaseModel):
    approved_workflow: Dict[str, Any]
    approved_sequence: Dict[str, Any]
    approved_state: Dict[str, Any]
    validation_status: str
    validation_id: str

class MetadataContract(BaseModel):
    execution_id: str
    engine_version: str = "FOLLOWUP-1.0"
    contract_version: str = "1.0"
    processing_timestamp: str
    validation_timestamp: str
    processing_status: str
    validation_status: str
    execution_metrics: Dict[str, Any] = Field(default_factory=dict)

class FollowUpExecutionPackageContract(BaseModel):
    formatted_followup_package: Dict[str, Any]
    metadata_package: MetadataContract
    validation_report: Dict[str, Any]
    processing_status: str
