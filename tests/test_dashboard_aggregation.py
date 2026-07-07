import pytest
from agents.dashboard.dashboard_contracts import DashboardAggregatedDataContract
from agents.dashboard.dashboard_managers import DashboardDataAggregationManager

@pytest.fixture
def mock_11_datasets():
    return {
        "search": {"execution_id": "S1"},
        "audit": {"execution_id": "A1"},
        "niche": {"execution_id": "N1"},
        "scoring": {"execution_id": "L1"},
        "contacts": {"execution_id": "C1"},
        "email_validation": {"execution_id": "E1"},
        "prototype": {"execution_id": "P1"},
        "personalized_email": {"execution_id": "PE1"},
        "followup": {"execution_id": "F1"},
        "crm": {"execution_id": "CR1"},
        "reporting": {"execution_id": "R1"}
    }

def test_dashboard_aggregation_success(mock_11_datasets):
    req = {
        "request_identifier": "REQ-TEST-1",
        "requested_view": "DEFAULT",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "request_parameters": {
            "aggregated_datasets": mock_11_datasets
        }
    }
    
    res = DashboardDataAggregationManager.aggregate_data(req)
    
    assert len(res["source_engine_references"]) == 11
    assert "search:S1" in res["source_engine_references"]
    
    # Contract validation check
    contract = DashboardAggregatedDataContract(**res)
    assert contract.collection_metadata["status"] == "CONSOLIDATED"

def test_dashboard_aggregation_missing_engines(mock_11_datasets):
    # Remove search engine
    mock_11_datasets.pop("search")
    
    req = {
        "request_identifier": "REQ-TEST-1",
        "requested_view": "DEFAULT",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "request_parameters": {
            "aggregated_datasets": mock_11_datasets
        }
    }
    
    with pytest.raises(ValueError, match="Missing required outputs from engines: search"):
        DashboardDataAggregationManager.aggregate_data(req)
