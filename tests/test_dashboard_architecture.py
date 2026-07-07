import pytest
from agents.dashboard.dashboard_agent import DashboardAgent
from agents.dashboard.dashboard_contracts import DashboardRequestContract, DashboardResponseContract
from agents.dashboard.dashboard_managers import (
    DashboardRequestManager,
    DashboardDataAggregationManager,
    DashboardModelManager,
    WidgetAssemblyManager,
    DashboardLayoutManager,
    DashboardValidationManager,
    DashboardPackagingManager,
    DashboardMetadataManager,
    DashboardExportPreparationManager,
    DashboardDeliveryPreparationManager
)

@pytest.fixture
def mock_11_datasets():
    return {
        "search": {}, "audit": {}, "niche": {}, "scoring": {},
        "contacts": {}, "email_validation": {}, "prototype": {},
        "personalized_email": {}, "followup": {}, "crm": {}, "reporting": {}
    }

@pytest.mark.asyncio
async def test_dashboard_architecture_imports(mock_11_datasets):
    agent = DashboardAgent()
    assert agent is not None
    
    mock_request = {
        "request_identifier": "REQ-DASH-100",
        "requested_view": "EXECUTIVE",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "request_parameters": {
            "aggregated_datasets": mock_11_datasets
        }
    }
    
    res = await agent.execute_dashboard(mock_request)
    assert res["success"] is True
    assert res["dashboard_identifier"].startswith("DASH-")
    assert res["view_format"] == "JSON"

def test_dashboard_managers_stubs(mock_11_datasets):
    res1 = DashboardRequestManager.process_request({
        "requested_view": "OPERATIONAL",
        "request_parameters": {"aggregated_datasets": mock_11_datasets}
    })
    assert res1["requested_view"] == "OPERATIONAL"

    res2 = DashboardDataAggregationManager.aggregate_data(res1)
    assert "aggregated_datasets" in res2

    res3 = DashboardModelManager.construct_model(res2)
    assert "dashboard_reporting_objects" in res3

    res4 = WidgetAssemblyManager.assemble_widgets(res3)
    assert res4["widget_count"] == 3

    res5 = DashboardLayoutManager.assemble_layout(res4)
    assert "layout_grid" in res5

    res6 = DashboardValidationManager.validate_dashboard(res5)
    assert res6["validation_status"] == "VALID"

    res7 = DashboardPackagingManager.package_dashboard(res6)
    assert "packaged_dashboard" in res7

    res8 = DashboardMetadataManager.generate_metadata(res7)
    assert res8["dashboard_identifier"].startswith("DASH-")

    res9 = DashboardExportPreparationManager.prepare_export(res7, res8)
    assert res9["export_readiness_status"] == "READY"

    res10 = DashboardDeliveryPreparationManager.prepare_delivery(res9)
    assert res10["delivery_readiness_status"] == "READY"
