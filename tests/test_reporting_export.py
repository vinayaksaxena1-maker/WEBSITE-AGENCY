import pytest
from agents.reporting.reporting_contracts import ExportPreparationContract
from agents.reporting.reporting_managers import ExportPreparationManager

def test_report_export_success():
    mock_packaged_report = {
        "packaged_report": {"content": {}},
        "packaging_descriptors": {"format": "JSON"}
    }
    
    mock_metadata = {
        "report_identifier": "REP-100",
        "metadata_version": "1.0.0",
        "processing_lineage": [],
        "source_references": [],
        "audit_information": {},
        "timestamp_information": {"generated_at": "2026-07-06T00:00:00Z"}
    }
    
    res = ExportPreparationManager.prepare_export(mock_packaged_report, mock_metadata)
    
    assert res["export_readiness_status"] == "READY"
    assert res["export_descriptors"]["destination"] == "OUTBOUND-API"
    
    # Contract validation check
    contract = ExportPreparationContract(**res)
    assert contract.attached_metadata.report_identifier == "REP-100"

def test_report_export_missing_packaged_report():
    with pytest.raises(ValueError, match="Missing packaged report"):
        ExportPreparationManager.prepare_export({}, {"report_identifier": "REP-100"})

def test_report_export_missing_identifier():
    with pytest.raises(ValueError, match="Missing metadata report identifier reference"):
        ExportPreparationManager.prepare_export({"packaged_report": {}}, {})
