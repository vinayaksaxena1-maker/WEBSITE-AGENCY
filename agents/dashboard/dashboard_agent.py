import logging
import uuid
from typing import Dict, Any
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
    DashboardDeliveryContract,
    DashboardResponseContract
)
from agents.dashboard.dashboard_managers import (
    DashboardRequestManager,
    DashboardDataAggregationManager,
    DashboardModelManager,
    WidgetAssemblyManager,
    DashboardLayoutManager,
    DashboardValidationManager,
    DashboardPackagingManager,
    DashboardMetadataManager,
    DashboardExportPreparationManager,
    DashboardDeliveryPreparationManager
)

logger = logging.getLogger("agency")

class DashboardAgent:
    def __init__(self):
        logger.info("DashboardAgent: Initializing Dashboard Engine.")

    async def execute_dashboard(self, raw_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the 10-stage Dashboard generation pipeline.
        Casts and validates each step output using EDK Pydantic contracts.
        """
        if not isinstance(raw_request, dict):
            return {
                "success": False,
                "error": "Workflow Precondition failed: Request payload must be a dictionary."
            }
        correlation_id = raw_request.get("request_identifier") or f"REQ-{uuid.uuid4().hex[:8].upper()}"
        try:
            logger.info(f"DashboardAgent: Starting execution workflow. [Correlation ID: {correlation_id}]")
            
            # Precondition Verification
            if not raw_request:
                raise ValueError("Workflow Precondition failed: Request payload cannot be empty.")
                
            # Stage 1: Request Processing
            req_res = DashboardRequestManager.process_request(raw_request)
            req_contract = DashboardRequestContract(**req_res)
            logger.info(f"DashboardAgent: Stage 1 - Request accepted. [Correlation ID: {correlation_id}]")
            
            # Stage 2: Data Aggregation
            agg_res = DashboardDataAggregationManager.aggregate_data(req_contract.model_dump())
            agg_contract = DashboardAggregatedDataContract(**agg_res)
            logger.info(f"DashboardAgent: Stage 2 - Data aggregated. [Correlation ID: {correlation_id}]")
            
            # Stage 3: Model Construction
            model_res = DashboardModelManager.construct_model(agg_contract.model_dump())
            model_contract = DashboardModelContract(**model_res)
            logger.info(f"DashboardAgent: Stage 3 - Model constructed. [Correlation ID: {correlation_id}]")
            
            # Stage 4: Widget Assembly
            widgets_res = WidgetAssemblyManager.assemble_widgets(model_contract.model_dump())
            widgets_contract = WidgetAssemblyContract(**widgets_res)
            logger.info(f"DashboardAgent: Stage 4 - Widgets assembled. [Correlation ID: {correlation_id}]")
            
            # Stage 5: Layout Assembly
            layout_res = DashboardLayoutManager.assemble_layout(widgets_contract.model_dump())
            layout_contract = DashboardLayoutContract(**layout_res)
            logger.info(f"DashboardAgent: Stage 5 - Layout assembled. [Correlation ID: {correlation_id}]")
            
            # Stage 6: Validation
            validation_res = DashboardValidationManager.validate_dashboard(layout_contract.model_dump())
            validation_contract = DashboardValidationContract(**validation_res)
            logger.info(f"DashboardAgent: Stage 6 - Dashboard validated. [Correlation ID: {correlation_id}]")
            
            # Stage 7: Packaging
            packaging_res = DashboardPackagingManager.package_dashboard(validation_contract.model_dump())
            packaging_contract = DashboardPackagingContract(**packaging_res)
            logger.info(f"DashboardAgent: Stage 7 - Dashboard packaged. [Correlation ID: {correlation_id}]")
            
            # Stage 8: Metadata Generation
            metadata_res = DashboardMetadataManager.generate_metadata(packaging_contract.model_dump())
            metadata_contract = DashboardMetadataContract(**metadata_res)
            logger.info(f"DashboardAgent: Stage 8 - Metadata generated. [Correlation ID: {correlation_id}]")
            
            # Stage 9: Export Preparation
            export_res = DashboardExportPreparationManager.prepare_export(packaging_contract.model_dump(), metadata_contract.model_dump())
            export_contract = DashboardExportContract(**export_res)
            logger.info(f"DashboardAgent: Stage 9 - Export ready. [Correlation ID: {correlation_id}]")
            
            # Stage 10: Delivery Preparation
            delivery_res = DashboardDeliveryPreparationManager.prepare_delivery(export_contract.model_dump())
            delivery_contract = DashboardDeliveryContract(**delivery_res)
            logger.info(f"DashboardAgent: Stage 10 - Delivery prepared. [Correlation ID: {correlation_id}]")
            
            # Assemble response
            response = DashboardResponseContract(
                success=True,
                dashboard_identifier=delivery_contract.attached_metadata.dashboard_identifier,
                view_format="JSON",
                assembled_metadata={"stages_completed": 10, "delivery_status": delivery_contract.delivery_readiness_status}
            )
            
            logger.info(f"DashboardAgent: Execution workflow completed successfully. [Correlation ID: {correlation_id}]")
            return response.model_dump()

        except Exception as e:
            logger.error(f"DashboardAgent: Orchestration pipeline failed: {e} [Correlation ID: {correlation_id}]", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
