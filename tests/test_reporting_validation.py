import pytest
from agents.reporting.reporting_contracts import ValidationContract
from agents.reporting.reporting_managers import ReportValidationManager

@pytest.fixture
def mock_assembled_report():
    return {
        "report_sections": [
            {"section_name": "Executive Summary", "content": {}},
            {"section_name": "Performance Metrics", "content": {}},
            {"section_name": "Normalized Lead Model", "content": {}}
        ],
        "executive_summary": {"highlights": []},
        "metrics": {
            "business_metrics": {
                "average_lead_score": 85.0
            }
        }
    }

def test_report_validation_success(mock_assembled_report):
    res = ReportValidationManager.validate_report(mock_assembled_report)
    
    assert res["validation_status"] == "VALID"
    assert res["schema_verification"] == "PASS"
    assert res["structural_verification"] == "PASS"
    
    # Contract validation check
    contract = ValidationContract(**res)
    assert contract.completeness_indicators["executive_summary_ok"] is True

def test_report_validation_missing_sections(mock_assembled_report):
    # Remove one section
    mock_assembled_report["report_sections"].pop()
    
    with pytest.raises(ValueError, match="Report sections are incomplete or missing"):
        ReportValidationManager.validate_report(mock_assembled_report)

def test_report_validation_invalid_lead_score(mock_assembled_report):
    # Set lead score to 0
    mock_assembled_report["metrics"]["business_metrics"]["average_lead_score"] = 0.0
    
    with pytest.raises(ValueError, match="Lead score metrics must be positive and non-zero"):
        ReportValidationManager.validate_report(mock_assembled_report)
