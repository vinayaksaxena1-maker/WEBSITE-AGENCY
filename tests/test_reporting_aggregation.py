import pytest
from pydantic import ValidationError
from agents.reporting.reporting_contracts import AggregatedDataContract, NormalizedDataContract
from agents.reporting.reporting_managers import DataAggregationManager, DataNormalizationManager

@pytest.fixture
def mock_engine_outputs():
    return {
        "search": {"domain": "teststore.com", "execution_id": "EX-SEARCH-01"},
        "audit": {"domain": "teststore.com", "execution_id": "EX-AUDIT-02"},
        "niche": {"niche": "eCommerce", "execution_id": "EX-NICHE-03"},
        "scoring": {"lead_score": 85.0, "execution_id": "EX-SCORE-04"},
        "contacts": {"extracted_email": "owner@teststore.com", "execution_id": "EX-CONTACT-05"},
        "email_validation": {"email": "owner@teststore.com", "validation_status": "VALID", "execution_id": "EX-VAL-06"},
        "prototype": {"prototype_id": "PROTO-872A", "execution_id": "EX-PROTO-07"},
        "personalized_email": {"subject": "Upgrade Proposal", "execution_id": "EX-EMAIL-08"},
        "followup": {"processing_status": "COMPLETED", "execution_id": "EX-FO-09"},
        "crm": {"crm_id": "CRM-881", "execution_id": "EX-CRM-10"}
    }

def test_aggregation_success(mock_engine_outputs):
    validated_req = {
        "request_identifier": "REQ-007",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "aggregated_datasets": mock_engine_outputs
    }
    
    aggregated_res = DataAggregationManager.aggregate_data(validated_req)
    assert aggregated_res["processing_references"]["request_id"] == "REQ-007"
    assert len(aggregated_res["source_engine_references"]) == 10
    
    # Contract check
    contract = AggregatedDataContract(**aggregated_res)
    assert contract.collection_metadata["status"] == "CONSOLIDATED"

def test_aggregation_missing_engines(mock_engine_outputs):
    # Remove search engine payload
    del mock_engine_outputs["search"]
    
    validated_req = {
        "request_identifier": "REQ-007",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "aggregated_datasets": mock_engine_outputs
    }
    
    with pytest.raises(ValueError, match="Missing outputs from engines: search"):
        DataAggregationManager.aggregate_data(validated_req)

def test_normalization_success(mock_engine_outputs):
    validated_req = {
        "request_identifier": "REQ-007",
        "request_timestamp": "2026-07-06T00:00:00Z",
        "aggregated_datasets": mock_engine_outputs
    }
    
    aggregated_res = DataAggregationManager.aggregate_data(validated_req)
    normalized_res = DataNormalizationManager.normalize_data(aggregated_res)
    
    # Assert values mapped properly
    objs = normalized_res["normalized_reporting_objects"]
    assert objs["target_domain"] == "teststore.com"
    assert objs["niche_classification"] == "eCommerce"
    assert objs["lead_score"] == 85.0
    assert objs["extracted_email"] == "owner@teststore.com"
    assert objs["email_validity"] == "VALID"
    assert objs["prototype_ref"] == "PROTO-872A"
    assert objs["crm_reference"] == "CRM-881"
    
    # Contract validation check
    contract = NormalizedDataContract(**normalized_res)
    assert contract.canonical_data_structures["type"] == "LeadPerformanceReport"
