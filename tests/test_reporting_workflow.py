import pytest
from agents.reporting.reporting_agent import ReportingAgent
from agents.reporting.reporting_contracts import ExportPreparationContract

@pytest.mark.asyncio
async def test_reporting_agent_workflow():
    agent = ReportingAgent()
    
    mock_datasets = {
        "search": {"domain": "abc.com"},
        "audit": {"domain": "abc.com"},
        "niche": {"niche": "SAAS"},
        "scoring": {"lead_score": 90.0},
        "contacts": {"extracted_email": "hello@abc.com"},
        "email_validation": {"validation_status": "VALID"},
        "prototype": {"prototype_id": "P1"},
        "personalized_email": {"subject": "Upgrade"},
        "followup": {"processing_status": "COMPLETED"},
        "crm": {"crm_id": "CRM-1"}
    }
    
    mock_request = {
        "request_identifier": "REQ-TEST-100",
        "requested_report_category": "OPERATIONAL",
        "report_parameters": {
            "detail_level": "HIGH",
            "aggregated_datasets": mock_datasets
        },
        "processing_options": {"compress": False}
    }
    
    result = await agent.execute_report(mock_request)
    
    assert result["success"] is True
    export_pkg = result["export_package"]
    assert export_pkg["export_readiness_status"] == "READY"
    
    # Structural compliance check using Pydantic
    contract = ExportPreparationContract(**export_pkg)
    assert contract.attached_metadata.metadata_version == "1.0.0"
    assert contract.packaging_information.packaging_descriptors["format"] == "JSON"
