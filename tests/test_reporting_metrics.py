import pytest
from agents.reporting.reporting_contracts import MetricsContract
from agents.reporting.reporting_managers import MetricsCompilationManager

@pytest.fixture
def mock_normalized_model():
    return {
        "normalized_reporting_objects": {
            "target_domain": "stores.com",
            "niche_classification": "eCommerce",
            "lead_score": 88.5,
            "extracted_email": "hello@stores.com",
            "email_validity": "VALID",
            "prototype_ref": "PROTO-1",
            "personalized_subject": "Upgrade proposal",
            "followup_sequence_status": "COMPLETED",
            "crm_reference": "CRM-1"
        }
    }

def test_metrics_compilation_success(mock_normalized_model):
    res = MetricsCompilationManager.compile_metrics(mock_normalized_model)
    
    assert res["business_metrics"]["average_lead_score"] == 88.5
    assert res["business_metrics"]["is_high_value"] is True
    assert res["campaign_metrics"]["emails_delivered"] == 1
    assert res["crm_metrics"]["crm_sync_status"] == "SUCCESS"
    
    # Contract validation check
    contract = MetricsContract(**res)
    assert contract.reporting_statistics["metric_count"] == 8

def test_metrics_compilation_out_of_bounds(mock_normalized_model):
    mock_normalized_model["normalized_reporting_objects"]["lead_score"] = 105.0
    
    with pytest.raises(ValueError, match="lead_score 105.0 is out of bounds"):
        MetricsCompilationManager.compile_metrics(mock_normalized_model)
