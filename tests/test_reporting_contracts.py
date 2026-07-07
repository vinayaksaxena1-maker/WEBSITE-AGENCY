import pytest
from pydantic import ValidationError
from agents.reporting.reporting_contracts import (
    ReportRequestContract,
    AggregatedDataContract,
    NormalizedDataContract,
    MetricsContract,
    ExecutiveSummaryContract,
    ReportAssemblyContract,
    ValidationContract,
    PackagingContract,
    MetadataContract,
    ExportPreparationContract
)

def test_report_request_validation():
    # Valid initiation
    req = ReportRequestContract(
        request_identifier="REQ-123",
        requested_report_category="CAMPAIGN",
        request_timestamp="2026-07-06T00:00:00Z"
    )
    assert req.request_identifier == "REQ-123"

    # Missing field
    with pytest.raises(ValidationError):
        ReportRequestContract(request_identifier="REQ-123")

def test_export_preparation_contract_validation():
    exec_summary = ExecutiveSummaryContract(
        business_overview="Overview info",
        operational_summary="Summary info",
        reporting_synopsis="Synopsis info"
    )
    
    metrics = MetricsContract(
        business_metrics={"conversion_rate": 0.12}
    )
    
    metadata = MetadataContract(
        report_identifier="REP-999"
    )
    
    packaging = PackagingContract(
        packaged_report={"content": "Report data"}
    )
    
    export_pkg = ExportPreparationContract(
        export_ready_report={"data": 123},
        attached_metadata=metadata,
        packaging_information=packaging,
        export_readiness_status="READY"
    )
    
    assert export_pkg.export_readiness_status == "READY"
    assert export_pkg.attached_metadata.report_identifier == "REP-999"
