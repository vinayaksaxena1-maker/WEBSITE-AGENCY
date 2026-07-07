import pytest
from pydantic import BaseModel, Field
from typing import Dict, Any, List

# Define the 7 Operational Engine Payload Contracts
class DiscoveryPayload(BaseModel):
    lead_id: str = Field(..., description="Unique Lead Tracking ID")
    session_id: str = Field(..., description="Session Identification ID")
    timestamp: str = Field(..., description="System Processing Timestamp")
    root_domain_url: str = Field(..., description="Validated Root Domain URL")
    industry_niche: str = Field(..., description="Target Business Industry Niche")
    discovery_vector: str = Field(..., description="Source Discovery Vector Code")
    status_flag: str = Field(default="PENDING_AUDIT", description="Status Flag")
    priority_score: int = Field(default=0, description="System Priority Classification Score")

class SiteDiagnosticsPayload(BaseModel):
    lead_id: str = Field(..., description="Target Lead ID")
    trace_id: str = Field(..., description="Global Trace Reference ID")
    end_timestamp: str = Field(..., description="Extraction End Timestamp")
    ssl_status: bool = Field(..., description="SSL Status Flag")
    mobile_compliant: bool = Field(..., description="Mobile Layout Compliance Indicator")
    page_latency: float = Field(..., description="Page Latency Score")
    seo_ranking: int = Field(..., description="Core SEO Visibility Ranking")
    technology_frameworks: List[str] = Field(..., description="Detected Technology Framework Array")
    layout_properties: Dict[str, Any] = Field(..., description="Identified Component Layout Properties JSON")
    structure_report: str = Field(..., description="Cleaned Structure Report")

class LeadPriorityPayload(BaseModel):
    lead_id: str = Field(..., description="Assigned Lead Reference ID")
    running_code: str = Field(..., description="Evaluation Running Code")
    timestamp: str = Field(..., description="Metric Generation Timestamp")
    defect_index: float = Field(..., description="Numeric Website Defect Index")
    opportunity_weight: float = Field(..., description="Business Opportunity Weight Model")
    priority_index: float = Field(..., description="Calculated Priority Index")
    decision_status: str = Field(..., description="Decision Status Flag (PROCEED/IGNORE)")
    design_strategy: str = Field(..., description="Recommended AI Design Strategy Code")

class VerifiedContactsPayload(BaseModel):
    lead_id: str = Field(..., description="Source Lead ID")
    run_ref_id: str = Field(..., description="Extraction Run Reference ID")
    timestamp: str = Field(..., description="Scanner Completion Timestamp")
    email_addresses: List[str] = Field(..., description="Raw Scraped Communication Address List")
    phone_numbers: List[str] = Field(..., description="Associated Phone Reference List")
    social_profiles: Dict[str, str] = Field(..., description="Public Social Profile Mapping Matrix")
    page_urls: List[str] = Field(..., description="Target Page URL Footprint List")
    integrity_flag: bool = Field(..., description="Processing Integrity Quality Flag")

class DeliverabilityAssessmentPayload(BaseModel):
    lead_id: str = Field(..., description="System Lead ID")
    trace_id: str = Field(..., description="Validation Operation Trace ID")
    timestamp: str = Field(..., description="Assessment Execution Timestamp")
    syntax_valid: bool = Field(..., description="Syntax Verification Result")
    mx_present: bool = Field(..., description="MX Routing Server Presence Flag")
    disposable_provider: bool = Field(..., description="Disposable Provider Check Code")
    deliverability_score: float = Field(..., description="Email Deliverability Metric")
    target_category: str = Field(..., description="Assigned Target Category")
    action_state: str = Field(..., description="Action Recommendation State (PROCEED/REJECT)")

class PrototypeBlueprintPayload(BaseModel):
    job_id: str = Field(..., description="Unique Job Tracking ID")
    lead_id: str = Field(..., description="Lead Binding ID")
    timestamp: str = Field(..., description="Generation Close Timestamp")
    storage_path: str = Field(..., description="Local Static Mockup Storage Path")
    preview_paths: List[str] = Field(..., description="Viewport Preview File Path Array")
    complexity_metric: float = Field(..., description="Automated Layout Complexity Metric")
    visual_score: float = Field(..., description="Computed Visual Hierarchy Score")
    match_index: float = Field(..., description="Core Component Match Index")
    layout_valid: bool = Field(..., description="Layout Validation Status Flag")

class OutreachPackagingPayload(BaseModel):
    transaction_id: str = Field(..., description="System Transaction ID")
    client_id: str = Field(..., description="Target Client ID")
    timestamp: str = Field(..., description="Packaging Complete Timestamp")
    subject: str = Field(..., description="Standardized Subject Copy String")
    body: str = Field(..., description="Personalized Message Body Text")
    attachment_ref: str = Field(..., description="Rendered Layout File Attachment Reference")
    safety_token: str = Field(..., description="Structural Safety Audit Token")
    validation_profile: Dict[str, Any] = Field(..., description="Validation Matrix Profile")
    deployment_status: str = Field(..., description="Queue Deployment Status Flag (READY_FOR_CRM)")

def test_operational_payload_contracts():
    disc = DiscoveryPayload(
        lead_id="L-1", session_id="S-1", timestamp="2026-07-07T00:00:00Z",
        root_domain_url="test.com", industry_niche="restaurants", discovery_vector="DDG"
    )
    assert disc.status_flag == "PENDING_AUDIT"

    diag = SiteDiagnosticsPayload(
        lead_id="L-1", trace_id="T-1", end_timestamp="2026-07-07T00:00:00Z",
        ssl_status=True, mobile_compliant=True, page_latency=1.2, seo_ranking=80,
        technology_frameworks=["react"], layout_properties={}, structure_report="Report"
    )
    assert diag.mobile_compliant is True
