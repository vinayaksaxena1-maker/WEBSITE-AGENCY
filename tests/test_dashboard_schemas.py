import pytest
from pydantic import ValidationError
from agents.dashboard.dashboard_contracts import (
    DashboardCanonicalPackageSchema,
    PackageHeaderSchema,
    DashboardLayoutSchema,
    WidgetCollectionSchema,
    DashboardSectionsSchema,
    SupportingInformationSchema,
    ValidationInformationSchema,
    MetadataSchema,
    ProcessingLineageSchema,
    PackageFooterSchema
)

def test_dashboard_canonical_package_schema_validation():
    # Valid canonical package structure
    canonical_payload = {
        "package_header": {
            "package_identifier": "PKG-1",
            "dashboard_identifier": "DASH-1",
            "dashboard_category": "OPERATIONAL",
            "generation_timestamp": "2026-07-07T00:00:00Z",
            "processing_identifier": "PROC-1",
            "dashboard_status": "COMPLETED"
        },
        "dashboard_layout": {},
        "widget_collections": {
            "kpi_widgets": [{"widget_id": "W-1", "value": "90"}]
        },
        "dashboard_sections": [
            {
                "section_identifier": "SEC-1",
                "section_name": "Main Section"
            }
        ],
        "supporting_information": {},
        "validation_information": {
            "validation_identifier": "VAL-1",
            "validation_status": "VALID",
            "validation_timestamp": "2026-07-07T00:00:00Z",
            "validation_results": {},
            "schema_verification": "PASS",
            "layout_verification": "PASS",
            "widget_verification": "PASS",
            "packaging_readiness_status": "READY"
        },
        "metadata": {
            "metadata_identifier": "META-1",
            "dashboard_identifier": "DASH-1",
            "package_identifier": "PKG-1",
            "processing_metadata": {},
            "version_metadata": {},
            "timestamp_metadata": {},
            "audit_metadata": {}
        },
        "processing_lineage": {
            "source_engine_references": [],
            "source_dataset_references": [],
            "dashboard_generation_references": [],
            "widget_assembly_references": [],
            "layout_assembly_references": [],
            "validation_references": [],
            "packaging_references": [],
            "metadata_references": [],
            "lineage_identifier": "LINE-1"
        },
        "package_footer": {
            "package_completion_status": "SUCCESS",
            "export_readiness_status": "READY",
            "delivery_readiness_status": "READY",
            "final_validation_status": "VALID",
            "package_timestamp": "2026-07-07T00:00:00Z",
            "package_integrity_indicator": "PASS"
        }
    }
    
    contract = DashboardCanonicalPackageSchema(**canonical_payload)
    assert contract.package_header.dashboard_category == "OPERATIONAL"
    assert contract.package_footer.package_integrity_indicator == "PASS"

def test_dashboard_canonical_package_schema_missing_header():
    # Missing package_header
    with pytest.raises(ValidationError):
        DashboardCanonicalPackageSchema(
            dashboard_layout={},
            widget_collections={},
            dashboard_sections=[],
            supporting_information={},
            validation_information={},
            metadata={},
            processing_lineage={},
            package_footer={}
        )
