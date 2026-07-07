from pydantic import BaseModel, Field
from typing import Dict, Any, List

class DashboardRequestContract(BaseModel):
    request_identifier: str = Field(..., description="Unique request identifier")
    requested_view: str = Field(..., description="Type of visual dashboard view")
    request_timestamp: str = Field(..., description="ISO UTC timestamp of request")
    request_parameters: Dict[str, Any] = Field(default_factory=dict, description="Custom parameters")
    processing_options: Dict[str, Any] = Field(default_factory=dict, description="Processing configurations")
    schema_version: str = Field(default="1.0.0", description="Data contract schema version")

class DashboardAggregatedDataContract(BaseModel):
    aggregated_datasets: Dict[str, Any] = Field(..., description="Consolidated upstream metrics")
    source_engine_references: List[str] = Field(..., description="Upstream engines names")
    dataset_identifiers: List[str] = Field(..., description="Unique dataset keys")
    collection_metadata: Dict[str, Any] = Field(..., description="Data collection metadata info")
    processing_references: Dict[str, Any] = Field(..., description="Traceability request keys")

class DashboardModelContract(BaseModel):
    dashboard_reporting_objects: Dict[str, Any] = Field(..., description="Normalized display targets")
    visualization_mappings: Dict[str, Any] = Field(..., description="Fields visual mappings")
    model_metadata: Dict[str, Any] = Field(..., description="Model construction metadata info")

class WidgetAssemblyContract(BaseModel):
    assembled_widgets: List[Dict[str, Any]] = Field(..., description="Assembled widget cards lists")
    widget_count: int = Field(..., description="Number of display widgets")
    assembly_status: str = Field(..., description="Assembly completion status")

class DashboardLayoutContract(BaseModel):
    layout_grid: Dict[str, Any] = Field(..., description="Layout placement positioning grid")
    widgets_information: WidgetAssemblyContract = Field(..., description="Reference widgets data")
    layout_metadata: Dict[str, Any] = Field(..., description="Layout packaging metadata")

class DashboardValidationContract(BaseModel):
    validation_status: str = Field(..., description="Validated status code")
    checks_run: int = Field(..., description="Number of integrity checks run")
    schema_verification: str = Field(..., description="Schema checks verification status")
    completeness_ok: bool = Field(..., description="Asserts completeness is verified")
    layout_ok: bool = Field(..., description="Asserts layout constraints are verified")
    validation_metadata: Dict[str, Any] = Field(..., description="Validation timestamp details")

class DashboardPackagingContract(BaseModel):
    packaged_dashboard: Dict[str, Any] = Field(..., description="Assembled package details")
    packaging_descriptors: Dict[str, Any] = Field(..., description="File formats and options")
    artifact_references: List[str] = Field(..., description="Reference target output files")
    internal_package_identifiers: List[str] = Field(..., description="Unique internal package IDs")

class DashboardMetadataContract(BaseModel):
    dashboard_identifier: str = Field(..., description="Unique dashboard identifier")
    metadata_version: str = Field(..., description="Metadata format version")
    processing_lineage: List[Dict[str, Any]] = Field(..., description="Lineage logs processing steps list")
    source_references: List[str] = Field(..., description="Platform references list")
    timestamp_information: Dict[str, Any] = Field(..., description="Time stamps registration details")

class DashboardExportContract(BaseModel):
    export_ready_report: Dict[str, Any] = Field(..., description="Export ready payload content")
    attached_metadata: DashboardMetadataContract = Field(..., description="Attached metadata details")
    packaging_information: DashboardPackagingContract = Field(..., description="Packaging details reference")
    export_descriptors: Dict[str, Any] = Field(..., description="Export target descriptors")
    export_readiness_status: str = Field(..., description="Final export readiness check status")

class DashboardDeliveryContract(BaseModel):
    delivery_ready_report: Dict[str, Any] = Field(..., description="Delivery content payload")
    attached_metadata: DashboardMetadataContract = Field(..., description="Attached metadata details")
    packaging_information: DashboardPackagingContract = Field(..., description="Packaging details reference")
    delivery_descriptors: Dict[str, Any] = Field(..., description="Delivery destination channels")
    delivery_readiness_status: str = Field(..., description="Final delivery readiness status")

class DashboardResponseContract(BaseModel):
    success: bool = Field(..., description="Indicates if dashboard assembly was completed successfully")
    dashboard_identifier: str = Field(..., description="Unique dashboard reference identifier")
    view_format: str = Field(..., description="Formatted visual layout representation")
    assembled_metadata: Dict[str, Any] = Field(default_factory=dict, description="Audit logging meta info")

class PackageHeaderSchema(BaseModel):
    package_identifier: str = Field(..., description="Package Identifier")
    dashboard_identifier: str = Field(..., description="Dashboard Identifier")
    dashboard_category: str = Field(..., description="Dashboard Category")
    schema_version: str = Field(default="1.0.0", description="Schema Version")
    package_version: str = Field(default="1.0.0", description="Package Version")
    dashboard_version: str = Field(default="1.0.0", description="Dashboard Version")
    generation_timestamp: str = Field(..., description="Generation Timestamp")
    processing_identifier: str = Field(..., description="Processing Identifier")
    dashboard_status: str = Field(..., description="Dashboard Status")

class DashboardLayoutSchema(BaseModel):
    dashboard_header: str = Field(default="DEFAULT-HEADER", description="Dashboard Header")
    navigation_area: str = Field(default="DEFAULT-NAV", description="Navigation Area")
    summary_section: str = Field(default="DEFAULT-SUMMARY", description="Summary Section")
    primary_widget_area: str = Field(default="DEFAULT-PRIMARY", description="Primary Widget Area")
    secondary_widget_area: str = Field(default="DEFAULT-SECONDARY", description="Secondary Widget Area")
    detail_section: str = Field(default="DEFAULT-DETAIL", description="Detail Section")
    status_section: str = Field(default="DEFAULT-STATUS", description="Status Section")
    footer_area: str = Field(default="DEFAULT-FOOTER", description="Footer Area")
    layout_references: List[str] = Field(default_factory=list, description="Layout References")
    layout_metadata: Dict[str, Any] = Field(default_factory=dict, description="Layout Metadata")

class WidgetCollectionSchema(BaseModel):
    summary_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Summary Widgets")
    kpi_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="KPI Widgets")
    metric_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Metric Widgets")
    chart_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Chart Widgets")
    table_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Table Widgets")
    pipeline_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Pipeline Widgets")
    crm_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="CRM Widgets")
    campaign_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Campaign Widgets")
    activity_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Activity Widgets")
    status_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Status Widgets")
    audit_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Audit Widgets")
    system_widgets: List[Dict[str, Any]] = Field(default_factory=list, description="System Widgets")

class DashboardSectionsSchema(BaseModel):
    section_identifier: str = Field(..., description="Section Identifier")
    section_name: str = Field(..., description="Section Name")
    widget_references: List[str] = Field(default_factory=list, description="Widget References")
    layout_references: List[str] = Field(default_factory=list, description="Layout References")
    source_references: List[str] = Field(default_factory=list, description="Source References")
    validation_references: List[str] = Field(default_factory=list, description="Validation References")
    processing_references: List[str] = Field(default_factory=list, description="Processing References")

class SupportingInformationSchema(BaseModel):
    supplemental_dashboard_data: Dict[str, Any] = Field(default_factory=dict, description="Supplemental Dashboard Data")
    supporting_references: List[str] = Field(default_factory=list, description="Supporting References")
    dashboard_notes: List[str] = Field(default_factory=list, description="Dashboard Notes")
    processing_context: Dict[str, Any] = Field(default_factory=dict, description="Processing Context")
    additional_dashboard_information: Dict[str, Any] = Field(default_factory=dict, description="Additional Dashboard Information")

class ValidationInformationSchema(BaseModel):
    validation_identifier: str = Field(..., description="Validation Identifier")
    validation_status: str = Field(..., description="Validation Status")
    validation_timestamp: str = Field(..., description="Validation Timestamp")
    validation_results: Dict[str, Any] = Field(..., description="Validation Results")
    schema_verification: str = Field(..., description="Schema Verification")
    layout_verification: str = Field(..., description="Layout Verification")
    widget_verification: str = Field(..., description="Widget Verification")
    packaging_readiness_status: str = Field(..., description="Packaging Readiness Status")

class MetadataSchema(BaseModel):
    metadata_identifier: str = Field(..., description="Metadata Identifier")
    dashboard_identifier: str = Field(..., description="Dashboard Identifier")
    package_identifier: str = Field(..., description="Package Identifier")
    schema_version: str = Field(default="1.0.0", description="Schema Version")
    package_version: str = Field(default="1.0.0", description="Package Version")
    dashboard_version: str = Field(default="1.0.0", description="Dashboard Version")
    processing_metadata: Dict[str, Any] = Field(..., description="Processing Metadata")
    version_metadata: Dict[str, Any] = Field(..., description="Version Metadata")
    timestamp_metadata: Dict[str, Any] = Field(..., description="Timestamp Metadata")
    audit_metadata: Dict[str, Any] = Field(..., description="Audit Metadata")

class ProcessingLineageSchema(BaseModel):
    source_engine_references: List[str] = Field(..., description="Source Engine References")
    source_dataset_references: List[str] = Field(..., description="Source Dataset References")
    dashboard_generation_references: List[str] = Field(..., description="Dashboard Generation References")
    widget_assembly_references: List[str] = Field(..., description="Widget Assembly References")
    layout_assembly_references: List[str] = Field(..., description="Layout Assembly References")
    validation_references: List[str] = Field(..., description="Validation References")
    packaging_references: List[str] = Field(..., description="Packaging References")
    metadata_references: List[str] = Field(..., description="Metadata References")
    lineage_identifier: str = Field(..., description="Lineage Identifier")

class PackageFooterSchema(BaseModel):
    package_completion_status: str = Field(..., description="Package Completion Status")
    export_readiness_status: str = Field(..., description="Export Readiness Status")
    delivery_readiness_status: str = Field(..., description="Delivery Readiness Status")
    final_validation_status: str = Field(..., description="Final Validation Status")
    package_timestamp: str = Field(..., description="Package Timestamp")
    package_integrity_indicator: str = Field(..., description="Package Integrity Indicator")

class DashboardCanonicalPackageSchema(BaseModel):
    package_header: PackageHeaderSchema = Field(..., description="Package Header Schema")
    dashboard_layout: DashboardLayoutSchema = Field(..., description="Dashboard Layout Schema")
    widget_collections: WidgetCollectionSchema = Field(..., description="Widget Collection Schema")
    dashboard_sections: List[DashboardSectionsSchema] = Field(..., description="Dashboard Sections Schema")
    supporting_information: SupportingInformationSchema = Field(..., description="Supporting Information Schema")
    validation_information: ValidationInformationSchema = Field(..., description="Validation Information Schema")
    metadata: MetadataSchema = Field(..., description="Metadata Schema")
    processing_lineage: ProcessingLineageSchema = Field(..., description="Processing Lineage Schema")
    package_footer: PackageFooterSchema = Field(..., description="Package Footer Schema")
