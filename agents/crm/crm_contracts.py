from pydantic import BaseModel, Field
from typing import Dict, Any, List
from agents.followup.followup_contracts import FollowUpExecutionPackageContract

class UnifiedInputContract(BaseModel):
    followup_execution_package: FollowUpExecutionPackageContract
    crm_config: Dict[str, Any] = Field(default_factory=dict)
    workflow_config: Dict[str, Any] = Field(default_factory=dict)
    agency_config: Dict[str, Any] = Field(default_factory=dict)
    brand_voice_config: Dict[str, Any] = Field(default_factory=dict)

class CRMContextContract(BaseModel):
    crm_id: str
    workflow_id: str
    customer_context: Dict[str, Any]
    execution_context: Dict[str, Any]
    crm_context: Dict[str, Any]
    lifecycle_context: Dict[str, Any]
    agency_context: Dict[str, Any]

class RelationshipContract(BaseModel):
    relationship_id: str
    crm_id: str
    crm_identity: Dict[str, Any]
    customer_references: Dict[str, Any]
    relationship_context: Dict[str, Any]
    relationship_metadata: Dict[str, Any]
    execution_references: Dict[str, Any]

class LifecycleContract(BaseModel):
    lifecycle_state: Dict[str, Any]
    relationship_state: Dict[str, Any]
    workflow_state: Dict[str, Any]
    processing_state: Dict[str, Any]
    lifecycle_metadata: Dict[str, Any]

class ValidatedCRMContract(BaseModel):
    approved_crm_record: Dict[str, Any]
    approved_relationship_information: Dict[str, Any]
    approved_lifecycle_information: Dict[str, Any]
    validation_status: str
    validation_identifier: str

class MetadataContract(BaseModel):
    execution_identifier: str
    engine_version: str = "CRM-1.0"
    contract_version: str = "1.0"
    processing_timestamp: str
    validation_timestamp: str
    processing_status: str
    validation_status: str
    execution_metrics: Dict[str, Any] = Field(default_factory=dict)

class CRMExecutionPackageContract(BaseModel):
    formatted_crm_package: Dict[str, Any]
    metadata_package: MetadataContract
    validation_report: Dict[str, Any]
    processing_status: str
