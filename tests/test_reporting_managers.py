from agents.reporting.reporting_managers import (
    ReportRequestManager,
    DataAggregationManager,
    DataNormalizationManager,
    MetricsCompilationManager,
    ExecutiveSummaryManager,
    ReportAssemblyManager,
    ReportValidationManager,
    ReportPackagingManager,
    ReportMetadataManager,
    ExportPreparationManager
)

def test_managers_stubs():
    # 1. ReportRequestManager
    res1 = ReportRequestManager.process_request({"req": 1})
    assert res1["request_processed"] is True
    assert res1["raw_request"] == {"req": 1}

    mock_datasets = {
        "search": {"domain": "abc.com"},
        "audit": {"domain": "abc.com"},
        "niche": {"niche": "SAAS"},
        "scoring": {"lead_score": 90.0},
        "contacts": {"extracted_email": "hello@abc.com"},
        "email_validation": {"validation_status": "VALID"},
        "prototype": {"prototype_id": "P1"},
        "personalized_email": {"subject": "Upgrade"},
        "followup": {"processing_status": "COMPLETED"},
        "crm": {"crm_id": "CRM-1"}
    }

    # 2. DataAggregationManager
    res2 = DataAggregationManager.aggregate_data({
        "request_identifier": "REQ-1",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "aggregated_datasets": mock_datasets
    })
    assert len(res2["source_engine_references"]) == 10

    # 3. DataNormalizationManager
    res3 = DataNormalizationManager.normalize_data(res2)
    assert "normalized_reporting_objects" in res3

    # 4. MetricsCompilationManager
    res4 = MetricsCompilationManager.compile_metrics(res3)
    assert "business_metrics" in res4

    # 5. ExecutiveSummaryManager
    res5 = ExecutiveSummaryManager.generate_summary(res4)
    assert "executive_highlights" in res5

    # 6. ReportAssemblyManager
    res6 = ReportAssemblyManager.assemble_report(res5, res4, res3)
    assert "report_sections" in res6

    # 7. ReportValidationManager
    res7 = ReportValidationManager.validate_report(res6)
    assert res7["validation_status"] == "VALID"

    # 8. ReportPackagingManager
    res8 = ReportPackagingManager.package_report(res7)
    assert "packaged_report" in res8

    # 9. ReportMetadataManager
    res9 = ReportMetadataManager.generate_metadata(res8)
    assert "report_identifier" in res9

    # 10. ExportPreparationManager
    res10 = ExportPreparationManager.prepare_export(res8, res9)
    assert res10["export_readiness_status"] == "READY"
