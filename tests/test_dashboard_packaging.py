import pytest
from agents.dashboard.dashboard_contracts import DashboardPackagingContract
from agents.dashboard.dashboard_managers import DashboardPackagingManager

def test_dashboard_packaging_success():
    val = {
        "validation_status": "VALID",
        "checks_run": 5,
        "schema_verification": "PASS",
        "completeness_ok": True,
        "layout_ok": True,
        "validation_metadata": {}
    }
    
    res = DashboardPackagingManager.package_dashboard(val)
    assert res["packaging_descriptors"]["version"] == "1.0.0"
    assert res["internal_package_identifiers"][0].startswith("PKG-")
    
    # Contract validation check
    contract = DashboardPackagingContract(**res)
    assert contract.packaging_descriptors["format"] == "JSON"

def test_dashboard_packaging_invalid_status():
    val = {
        "validation_status": "INVALID",
        "checks_run": 5,
        "schema_verification": "FAIL",
        "completeness_ok": False,
        "layout_ok": False,
        "validation_metadata": {}
    }
    
    with pytest.raises(ValueError, match="Dashboard validation status is not 'VALID'"):
        DashboardPackagingManager.package_dashboard(val)

def test_dashboard_packaging_invalid_type():
    with pytest.raises(TypeError):
        DashboardPackagingManager.package_dashboard("not-a-dict") # type: ignore
