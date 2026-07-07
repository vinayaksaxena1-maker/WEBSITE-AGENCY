import pytest
from pydantic import ValidationError
from agents.dashboard.dashboard_contracts import (
    DashboardRequestContract,
    DashboardAggregatedDataContract,
    DashboardModelContract,
    WidgetAssemblyContract,
    DashboardLayoutContract,
    DashboardValidationContract,
    DashboardPackagingContract,
    DashboardMetadataContract,
    DashboardExportContract,
    DashboardDeliveryContract
)

def test_dashboard_request_contract_validation():
    # Missing request_identifier and requested_view
    with pytest.raises(ValidationError):
        DashboardRequestContract(request_timestamp="2026-07-06T00:00:00Z")
        
    contract = DashboardRequestContract(
        request_identifier="REQ-1",
        requested_view="DEFAULT",
        request_timestamp="2026-07-06T00:00:00Z"
    )
    assert contract.schema_version == "1.0.0"

def test_dashboard_aggregated_data_contract_validation():
    # Missing fields
    with pytest.raises(ValidationError):
        DashboardAggregatedDataContract(aggregated_datasets={})
        
    contract = DashboardAggregatedDataContract(
        aggregated_datasets={},
        source_engine_references=["Search"],
        dataset_identifiers=["D1"],
        collection_metadata={"status": "OK"},
        processing_references={"req": "R1"}
    )
    assert contract.collection_metadata["status"] == "OK"
