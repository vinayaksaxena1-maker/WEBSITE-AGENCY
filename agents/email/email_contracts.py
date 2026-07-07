from pydantic import BaseModel, Field
from typing import Dict, Any, List

class LeadProfileContract(BaseModel):
    domain: str
    niche: str

class AuditReportContract(BaseModel):
    audit_score: int = Field(..., ge=0, le=100)
    mobile_score: int = Field(..., ge=0, le=100)
    speed_score: int = Field(..., ge=0, le=100)

class PrototypeReportContract(BaseModel):
    prototype_url: str

class ContactInfoContract(BaseModel):
    name: str
    email: str

class UnifiedInputPackage(BaseModel):
    lead_profile: LeadProfileContract
    audit_report: AuditReportContract
    prototype_report: PrototypeReportContract
    contact_info: ContactInfoContract
    agency_config: Dict[str, Any] = Field(default_factory=dict)

class UnifiedBusinessContext(BaseModel):
    target_domain: str
    target_niche: str
    target_email: str
    audit_score: int
    mobile_score: int
    speed_score: int
    prototype_url: str
    contact_name: str

class PersonalizationContext(BaseModel):
    target_email: str
    contact_name: str
    company_name: str
    target_niche: str
    modernization_hook: str
    niche_terminology: str
    prototype_url: str
    audit_score: int

class AIPromptPackage(BaseModel):
    prompt_subject: str
    prompt_body: str
    target_email: str
    variables: Dict[str, Any]

class GeneratedEmailDraft(BaseModel):
    subject: str
    body: str
    target_email: str

class ValidatedEmailDraft(BaseModel):
    subject: str
    body: str
    target_email: str

class FormattedEmailPackage(BaseModel):
    subject: str
    html_body: str
    text_body: str
    target_email: str

class ValidationReportContract(BaseModel):
    validation_id: str
    status: str
    checked_at: str
    structural_validation: str
    personalization_validation: str
    communication_validation: str
    factual_validation: str
    formatting_validation: str
    overall_validation_result: str
    errors: List[str] = Field(default_factory=list)

class ProcessingMetadataContract(BaseModel):
    processing_timestamp: str
    processing_status: str
    execution_duration_sec: float
    completion_status: str

class PublicationMetadataContract(BaseModel):
    publication_status: str
    publication_timestamp: str
    output_package_identifier: str

class FinalEmailPackageMetadata(BaseModel):
    execution_id: str
    engine_version: str = "EMAIL-1.0"
    validation_status: str
    validation_report: ValidationReportContract
    processing_metadata: ProcessingMetadataContract
    publication_metadata: PublicationMetadataContract

class FinalEmailPackage(BaseModel):
    email_payload: FormattedEmailPackage
    metadata: FinalEmailPackageMetadata
