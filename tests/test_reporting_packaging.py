import pytest
from agents.reporting.reporting_contracts import PackagingContract
from agents.reporting.reporting_managers import ReportPackagingManager

def test_report_packaging_success():
    mock_validated_report = {
        "validation_status": "VALID",
        "schema_verification": "PASS"
    }
    
    res = ReportPackagingManager.package_report(mock_validated_report)
    
    assert res["packaging_descriptors"]["format"] == "JSON"
    assert len(res["internal_package_identifiers"]) == 1
    assert res["internal_package_identifiers"][0].startswith("PKG-")
    
    # Contract validation check
    contract = PackagingContract(**res)
    assert contract.packaging_metadata["packaged_at"] == "2026-07-06T00:00:00Z"

def test_report_packaging_invalid_status():
    mock_validated_report = {
        "validation_status": "INVALID"
    }
    
    with pytest.raises(ValueError, match="Validated report status must be VALID"):
        ReportPackagingManager.package_report(mock_validated_report)
