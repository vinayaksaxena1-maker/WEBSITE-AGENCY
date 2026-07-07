import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from core.logger import logger

# Import contracts
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

# Import managers
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

class ReportingAgent:
    def __init__(self):
        self.name = "Reporting Engine"

    async def execute_report(self, raw_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates sequential execution of the Reporting Engine workflow (Phase 11.4).
        Enforces execution sequence and contract validation at checkpoints.
        """
        logger.info("ReportingAgent: Initiating Reporting Engine execution workflow.")
        try:
            # 1. Report Request processing & contract validation
            req_res = ReportRequestManager.process_request(raw_request)
            request_contract = ReportRequestContract(
                request_identifier=raw_request.get("request_identifier") or f"REQ-{uuid.uuid4().hex[:8].upper()}",
                requested_report_category=raw_request.get("requested_report_category") or "CAMPAIGN",
                report_parameters=raw_request.get("report_parameters") or {},
                processing_options=raw_request.get("processing_options") or {},
                request_timestamp=raw_request.get("request_timestamp") or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            )
            logger.info(f"ReportingAgent: Stage 1 - Request validated (ID: {request_contract.request_identifier}).")

            # 2. Data Aggregation
            agg_res = DataAggregationManager.aggregate_data(request_contract.model_dump())
            agg_contract = AggregatedDataContract(**agg_res)
            logger.info("ReportingAgent: Stage 2 - Data aggregated successfully.")

            # 3. Data Normalization
            norm_res = DataNormalizationManager.normalize_data(agg_contract.model_dump())
            norm_contract = NormalizedDataContract(**norm_res)
            logger.info("ReportingAgent: Stage 3 - Data normalized.")

            # 4. Metrics Compilation
            metrics_res = MetricsCompilationManager.compile_metrics(norm_contract.model_dump())
            metrics_contract = MetricsContract(**metrics_res)
            logger.info("ReportingAgent: Stage 4 - Metrics compiled.")

            # 5. Executive Summary Generation
            summary_res = ExecutiveSummaryManager.generate_summary(metrics_contract.model_dump())
            summary_contract = ExecutiveSummaryContract(**summary_res)
            logger.info("ReportingAgent: Stage 5 - Executive summary generated.")

            # 6. Report Assembly
            assembly_res = ReportAssemblyManager.assemble_report(
                summary_contract.model_dump(),
                metrics_contract.model_dump(),
                norm_contract.model_dump()
            )
            assembly_contract = ReportAssemblyContract(**assembly_res)
            logger.info("ReportingAgent: Stage 6 - Report assembled.")

            # 7. Report Validation
            validation_res = ReportValidationManager.validate_report(assembly_contract.model_dump())
            validation_contract = ValidationContract(**validation_res)
            logger.info("ReportingAgent: Stage 7 - Report validation checks passed.")

            # 8. Report Packaging
            packaging_res = ReportPackagingManager.package_report(validation_contract.model_dump())
            packaging_contract = PackagingContract(**packaging_res)
            logger.info("ReportingAgent: Stage 8 - Report packaged.")

            # 9. Metadata Generation
            metadata_res = ReportMetadataManager.generate_metadata(packaging_contract.model_dump())
            metadata_contract = MetadataContract(**metadata_res)
            logger.info(f"ReportingAgent: Stage 9 - Metadata compiled (ID: {metadata_contract.report_identifier}).")

            # 10. Export Preparation
            export_res = ExportPreparationManager.prepare_export(packaging_contract.model_dump(), metadata_contract.model_dump())
            export_contract = ExportPreparationContract(**export_res)
            logger.info("ReportingAgent: Stage 10 - Export package finalized.")

            return {
                "success": True,
                "export_package": export_contract.model_dump()
            }

        except Exception as e:
            logger.error(f"ReportingAgent: Orchestration pipeline failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
