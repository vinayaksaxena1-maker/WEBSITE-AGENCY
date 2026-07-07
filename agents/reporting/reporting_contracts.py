from pydantic import BaseModel, Field
from typing import Dict, Any, List

class ReportRequestContract(BaseModel):
    request_identifier: str
    requested_report_category: str
    report_parameters: Dict[str, Any] = Field(default_factory=dict)
    processing_options: Dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0.0"
    request_timestamp: str

class AggregatedDataContract(BaseModel):
    aggregated_datasets: Dict[str, Any]
    source_engine_references: List[str] = Field(default_factory=list)
    dataset_identifiers: List[str] = Field(default_factory=list)
    collection_metadata: Dict[str, Any] = Field(default_factory=dict)
    processing_references: Dict[str, Any] = Field(default_factory=dict)

class NormalizedDataContract(BaseModel):
    normalized_reporting_objects: Dict[str, Any]
    standardized_field_mappings: Dict[str, Any] = Field(default_factory=dict)
    canonical_data_structures: Dict[str, Any] = Field(default_factory=dict)
    normalization_metadata: Dict[str, Any] = Field(default_factory=dict)
    schema_references: Dict[str, Any] = Field(default_factory=dict)

class MetricsContract(BaseModel):
    business_metrics: Dict[str, Any] = Field(default_factory=dict)
    operational_metrics: Dict[str, Any] = Field(default_factory=dict)
    campaign_metrics: Dict[str, Any] = Field(default_factory=dict)
    pipeline_metrics: Dict[str, Any] = Field(default_factory=dict)
    crm_metrics: Dict[str, Any] = Field(default_factory=dict)
    reporting_statistics: Dict[str, Any] = Field(default_factory=dict)

class ExecutiveSummaryContract(BaseModel):
    executive_highlights: List[str] = Field(default_factory=list)
    business_overview: str
    operational_summary: str
    reporting_synopsis: str
    summary_metadata: Dict[str, Any] = Field(default_factory=dict)

class ReportAssemblyContract(BaseModel):
    report_sections: List[Dict[str, Any]] = Field(default_factory=list)
    executive_summary: ExecutiveSummaryContract
    metrics: MetricsContract
    supporting_information: Dict[str, Any] = Field(default_factory=dict)
    structural_hierarchy: Dict[str, Any] = Field(default_factory=dict)
    assembly_references: Dict[str, Any] = Field(default_factory=dict)

class ValidationContract(BaseModel):
    validation_status: str
    validation_results: Dict[str, Any] = Field(default_factory=dict)
    schema_verification: str
    structural_verification: str
    completeness_indicators: Dict[str, Any] = Field(default_factory=dict)
    validation_metadata: Dict[str, Any] = Field(default_factory=dict)

class PackagingContract(BaseModel):
    packaged_report: Dict[str, Any]
    packaging_descriptors: Dict[str, Any] = Field(default_factory=dict)
    artifact_references: List[str] = Field(default_factory=list)
    internal_package_identifiers: List[str] = Field(default_factory=list)
    packaging_metadata: Dict[str, Any] = Field(default_factory=dict)

class MetadataContract(BaseModel):
    report_identifier: str
    metadata_version: str = "1.0.0"
    processing_lineage: List[Dict[str, Any]] = Field(default_factory=list)
    source_references: List[str] = Field(default_factory=list)
    audit_information: Dict[str, Any] = Field(default_factory=dict)
    timestamp_information: Dict[str, str] = Field(default_factory=dict)

class ExportPreparationContract(BaseModel):
    export_ready_report: Dict[str, Any]
    attached_metadata: MetadataContract
    packaging_information: PackagingContract
    export_descriptors: Dict[str, Any] = Field(default_factory=dict)
    export_readiness_status: str
