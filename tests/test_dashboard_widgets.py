import pytest
from pydantic import ValidationError
from agents.dashboard.dashboard_contracts import WidgetAssemblyContract
from agents.dashboard.dashboard_managers import WidgetAssemblyManager

def test_widget_assembly_success():
    model = {
        "dashboard_reporting_objects": {
            "lead_score": 92.5,
            "niche_classification": "Automotive",
            "email_status": "VALID"
        },
        "visualization_mappings": {},
        "model_metadata": {}
    }
    
    res = WidgetAssemblyManager.assemble_widgets(model)
    assert res["widget_count"] == 3
    assert res["assembled_widgets"][0]["value"] == "92.5"
    assert res["assembled_widgets"][1]["value"] == "Automotive"
    assert res["assembled_widgets"][2]["value"] == "VALID"
    
    # Contract validation check
    contract = WidgetAssemblyContract(**res)
    assert contract.assembly_status == "COMPLETED"

def test_widget_assembly_invalid_input():
    with pytest.raises(TypeError):
        WidgetAssemblyManager.assemble_widgets("not-a-dict") # type: ignore
