import pytest
from agents.dashboard.dashboard_contracts import DashboardValidationContract
from agents.dashboard.dashboard_managers import DashboardValidationManager

@pytest.fixture
def mock_valid_layout():
    return {
        "layout_grid": {
            "rows": 1,
            "columns": 3,
            "placement": [
                {"widget_id": "WIDGET-SCORE", "row": 1, "col": 1},
                {"widget_id": "WIDGET-NICHE", "row": 1, "col": 2},
                {"widget_id": "WIDGET-EMAIL", "row": 1, "col": 3}
            ]
        },
        "widgets_information": {
            "assembled_widgets": [],
            "widget_count": 0,
            "assembly_status": "COMPLETED"
        },
        "layout_metadata": {
            "grid_version": "1.0",
            "total_positions": 3
        }
    }

def test_dashboard_validation_success(mock_valid_layout):
    res = DashboardValidationManager.validate_dashboard(mock_valid_layout)
    assert res["validation_status"] == "VALID"
    assert res["checks_run"] == 5
    
    # Contract validation check
    contract = DashboardValidationContract(**res)
    assert contract.completeness_ok is True

def test_dashboard_validation_missing_mandatory(mock_valid_layout):
    # Remove one mandatory widget
    mock_valid_layout["layout_grid"]["placement"][0]["widget_id"] = "WIDGET-OTHER"
    
    with pytest.raises(ValueError, match="Missing mandatory visual section widgets: WIDGET-SCORE"):
        DashboardValidationManager.validate_dashboard(mock_valid_layout)

def test_dashboard_validation_grid_version_mismatch(mock_valid_layout):
    mock_valid_layout["layout_metadata"]["grid_version"] = "2.0"
    
    with pytest.raises(ValueError, match="Unsupported grid version '2.0'"):
        DashboardValidationManager.validate_dashboard(mock_valid_layout)
