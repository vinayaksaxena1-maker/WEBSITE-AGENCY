import pytest
from pydantic import ValidationError
from agents.dashboard.dashboard_contracts import DashboardLayoutContract
from agents.dashboard.dashboard_managers import DashboardLayoutManager

def test_layout_assembly_success():
    widgets_package = {
        "assembled_widgets": [
            {"widget_id": "W-A", "type": "KPI-CARD", "title": "Score", "value": "90"},
            {"widget_id": "W-B", "type": "TEXT-BOX", "title": "Niche", "value": "Tech"}
        ],
        "widget_count": 2,
        "assembly_status": "COMPLETED"
    }
    
    res = DashboardLayoutManager.assemble_layout(widgets_package)
    assert res["layout_grid"]["columns"] == 2
    assert len(res["layout_grid"]["placement"]) == 2
    assert res["layout_grid"]["placement"][0]["widget_id"] == "W-A"
    assert res["layout_grid"]["placement"][0]["row"] == 1
    assert res["layout_grid"]["placement"][0]["col"] == 1
    assert res["layout_grid"]["placement"][1]["widget_id"] == "W-B"
    assert res["layout_grid"]["placement"][1]["col"] == 2
    
    # Contract validation check
    contract = DashboardLayoutContract(**res)
    assert contract.layout_metadata["total_positions"] == 2

def test_layout_assembly_invalid_input():
    with pytest.raises(TypeError):
        DashboardLayoutManager.assemble_layout("not-a-dict") # type: ignore
