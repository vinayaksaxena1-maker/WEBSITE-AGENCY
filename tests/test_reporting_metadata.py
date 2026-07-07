import pytest
from agents.reporting.reporting_contracts import MetadataContract
from agents.reporting.reporting_managers import ReportMetadataManager

def test_report_metadata_success():
    mock_packaged_report = {
        "packaged_report": {"content": {}},
        "packaging_descriptors": {"format": "JSON"}
    }
    
    res = ReportMetadataManager.generate_metadata(mock_packaged_report)
    
    assert res["metadata_version"] == "1.0.0"
    assert len(res["processing_lineage"]) == 7
    assert res["report_identifier"].startswith("REP-")
    assert res["audit_information"]["compliance_check"] == "PASS"
    
    # Contract validation check
    contract = MetadataContract(**res)
    assert contract.timestamp_information["generated_at"] == "2026-07-06T00:00:00Z"

def test_report_metadata_missing_content():
    mock_packaged_report = {
        "packaging_descriptors": {"format": "JSON"}
    }
    
    with pytest.raises(ValueError, match="Missing packaged report content"):
        ReportMetadataManager.generate_metadata(mock_packaged_report)
