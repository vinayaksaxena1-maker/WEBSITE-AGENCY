import logging
from typing import Dict, Any
from agents.notification.notification_contracts import (
    NotificationRequestContract,
    NotificationPayloadContract,
    RecipientChannelContract,
    TemplateMappingContract,
    RoutingDispatchContract,
    QueueSchedulingContract,
    DeliveryExecutionContract,
    DeliveryValidationContract,
    NotificationMetadataContract,
    AcknowledgementContract,
    NotificationResponseContract
)
from agents.notification.notification_managers import (
    NotificationRequestManager,
    NotificationPayloadManager,
    RecipientChannelManager,
    TemplateMappingManager,
    RoutingDispatchManager,
    QueueSchedulingManager,
    DeliveryExecutionManager,
    DeliveryValidationManager,
    NotificationMetadataManager,
    AcknowledgementManager
)

logger = logging.getLogger("agency")

class NotificationAgent:
    def __init__(self):
        logger.info("NotificationAgent: Initializing Notification Engine Architecture.")

    async def execute_notification(self, raw_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the 10-stage Notification routing pipeline.
        """
        try:
            logger.info("NotificationAgent: Starting execution workflow.")
            
            # Precondition checks
            if not isinstance(raw_request, dict):
                raise ValueError("Notification request payload must be a dictionary.")
            if not raw_request:
                raise ValueError("Notification request payload cannot be empty.")
            
            # Stage 1: Request Processing
            req_raw = NotificationRequestManager.process_request(raw_request)
            req_contract = NotificationRequestContract(**req_raw)
            
            # Stage 2: Payload Validation
            payload_raw = NotificationPayloadManager.validate_payload(req_contract.model_dump())
            payload_contract = NotificationPayloadContract(**payload_raw)
            
            # Stage 3: Recipient & Channel Validation
            recipient_raw = RecipientChannelManager.validate_recipient(payload_contract.model_dump())
            recipient_contract = RecipientChannelContract(**recipient_raw)
            
            # Stage 4: Template Mapping & Rendering
            template_raw = TemplateMappingManager.map_template(recipient_contract.model_dump())
            template_contract = TemplateMappingContract(**template_raw)
            
            # Stage 5: Routing & Dispatch Decision
            routing_raw = RoutingDispatchManager.resolve_routing(template_contract.model_dump())
            routing_contract = RoutingDispatchContract(**routing_raw)
            
            # Stage 6: Queueing & Scheduling
            queue_raw = QueueSchedulingManager.enqueue_notification(routing_contract.model_dump())
            queue_contract = QueueSchedulingContract(**queue_raw)
            
            # Stage 7: Delivery Execution / Dispatch
            delivery_raw = DeliveryExecutionManager.execute_delivery(queue_contract.model_dump())
            delivery_contract = DeliveryExecutionContract(**delivery_raw)
            
            # Stage 8: Delivery Validation & Policy Check
            validation_raw = DeliveryValidationManager.validate_delivery(delivery_contract.model_dump())
            validation_contract = DeliveryValidationContract(**validation_raw)
            
            # Stage 9: Audit Metadata & Lineage Generation
            metadata_raw = NotificationMetadataManager.generate_metadata(validation_contract.model_dump())
            metadata_contract = NotificationMetadataContract(**metadata_raw)
            
            # Stage 10: Acknowledgement & Status Delivery
            ack_raw = AcknowledgementManager.record_acknowledgement(metadata_contract.model_dump())
            ack_contract = AcknowledgementContract(**ack_raw)
            
            # Assemble response
            response = NotificationResponseContract(
                success=True,
                notification_identifier=ack_contract.metadata.notification_identifier,
                delivery_status=ack_contract.delivery_readiness_status,
                assembled_metadata={"stages_completed": 10}
            )
            
            logger.info("NotificationAgent: Execution workflow completed successfully.")
            return response.model_dump()

        except Exception as e:
            logger.error(f"NotificationAgent: Orchestration pipeline failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
