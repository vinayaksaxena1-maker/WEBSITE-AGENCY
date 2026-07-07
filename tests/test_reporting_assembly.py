import pytest
from agents.reporting.reporting_contracts import ExecutiveSummaryContract, ReportAssemblyContract
from agents.reporting.reporting_managers import ExecutiveSummaryManager, ReportAssemblyManager

@pytest.fixture
def mock_metrics():
    return {
        "business_metrics": {
            "average_lead_score": 92.0,
            "is_high_value": True
        },
        "operational_metrics": {},
        "campaign_metrics": {},
        "pipeline_metrics": {},
        "crm_metrics": {},
        "reporting_statistics": {}
    }

@pytest.fixture
def mock_normalized():
    return {
        "normalized_reporting_objects": {"target_domain": "test.com"},
        "standardized_field_mappings": {},
        "canonical_data_structures": {},
        "normalization_metadata": {},
        "schema_references": {}
    }

def test_summary_generation_success(mock_metrics):
    res = ExecutiveSummaryManager.generate_summary(mock_metrics)
    
    assert "92.0" in res["executive_highlights"][0]
    assert "High value" in res["executive_highlights"][1]
    
    # Contract validation check
    contract = ExecutiveSummaryContract(**res)
    assert contract.business_overview.startswith("Lead analysis overview")

def test_report_assembly_success(mock_metrics, mock_normalized):
    summary_res = ExecutiveSummaryManager.generate_summary(mock_metrics)
    
    res = ReportAssemblyManager.assemble_report(summary_res, mock_metrics, mock_normalized)
    
    assert len(res["report_sections"]) == 3
    assert res["structural_hierarchy"]["root"] == "EnterprisePerformanceReport"
    
    # Contract validation check
    contract = ReportAssemblyContract(**res)
    assert contract.metrics.business_metrics["average_lead_score"] == 92.0
