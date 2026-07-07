import pytest
from pydantic import ValidationError
from agents.dashboard.dashboard_contracts import DashboardMetadataContract
from agents.dashboard.dashboard_managers import DashboardMetadataManager

def test_dashboard_metadata_success():
    packaged = {
        "packaged_dashboard": {},
        "packaging_descriptors": {},
        "artifact_references": [],
        "internal_package_identifiers": ["PKG-A"]
    }
    
    res = DashboardMetadataManager.generate_metadata(packaged)
    assert res["dashboard_identifier"].startswith("DASH-")
    assert res["metadata_version"] == "1.0.0"
    assert len(res["processing_lineage"]) == 3
    assert "search" in res["source_references"]
    
    # Contract validation check
    contract = DashboardMetadataContract(**res)
    assert contract.metadata_version == "1.0.0"

def test_dashboard_metadata_missing_package_ids():
    packaged = {
        "packaged_dashboard": {},
        "packaging_descriptors": {},
        "artifact_references": [],
        "internal_package_identifiers": []
    }
    
    with pytest.raises(ValueError, match="must contain at least one package ID"):
        DashboardMetadataManager.generate_metadata(packaged)

def test_dashboard_metadata_invalid_type():
    with pytest.raises(TypeError):
        DashboardMetadataManager.generate_metadata("not-a-dict") # type: ignore
