import pytest
from agents.dashboard.dashboard_agent import DashboardAgent

@pytest.fixture
def mock_11_datasets():
    return {
        "search": {}, "audit": {}, "niche": {}, "scoring": {},
        "contacts": {}, "email_validation": {}, "prototype": {},
        "personalized_email": {}, "followup": {}, "crm": {}, "reporting": {}
    }

@pytest.mark.asyncio
async def test_dashboard_workflow_success(mock_11_datasets):
    agent = DashboardAgent()
    
    mock_request = {
        "request_identifier": "REQ-FLOW-100",
        "requested_view": "CAMPAIGN",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "request_parameters": {
            "aggregated_datasets": mock_11_datasets
        }
    }
    
    res = await agent.execute_dashboard(mock_request)
    assert res["success"] is True
    assert res["dashboard_identifier"].startswith("DASH-")

@pytest.mark.asyncio
async def test_dashboard_workflow_precondition_failures(mock_11_datasets):
    agent = DashboardAgent()
    
    # 1. Invalid category should raise ValueError inside RequestManager
    mock_request1 = {
        "request_identifier": "REQ-FLOW-200",
        "requested_view": "INVALID-CAT",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "request_parameters": {
            "aggregated_datasets": mock_11_datasets
        }
    }
    res1 = await agent.execute_dashboard(mock_request1)
    assert res1["success"] is False
    assert "Unsupported view category" in res1["error"]
    
    # 2. Empty payload should raise ValueError
    res2 = await agent.execute_dashboard({})
    assert res2["success"] is False
    assert "payload cannot be empty" in res2["error"]

    # 3. Non-dictionary payload should raise TypeError
    res3 = await agent.execute_dashboard("not-a-dict") # type: ignore
    assert res3["success"] is False
    assert "must be a dictionary" in res3["error"]
