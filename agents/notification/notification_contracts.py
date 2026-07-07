from pydantic import BaseModel, Field
from typing import Dict, Any, List

class NotificationRequestContract(BaseModel):
    request_identifier: str = Field(..., description="Unique request identifier")
    recipient_identifier: str = Field(..., description="Recipient address identifier")
    notification_type: str = Field(..., description="Notification channel type (EMAIL, SMS, LOG)")
    request_timestamp: str = Field(..., description="ISO UTC timestamp of request")
    request_parameters: Dict[str, Any] = Field(default_factory=dict, description="Request parameters dict details")

class NotificationPayloadContract(BaseModel):
    payload_data: Dict[str, Any] = Field(..., description="Notification payload contents subject and body")
    payload_validated: bool = Field(..., description="Asserts payload size and formatting are valid")
    validated_request: NotificationRequestContract = Field(..., description="Attached validated request reference")

class RecipientChannelContract(BaseModel):
    recipient_details: Dict[str, Any] = Field(..., description="Recipient profile and channels credentials verification")
    recipient_validated: bool = Field(..., description="Asserts recipient credentials verified")
    payload: NotificationPayloadContract = Field(..., description="Attached validated payload reference")

class TemplateMappingContract(BaseModel):
    rendered_content: Dict[str, Any] = Field(..., description="Rendered template content results")
    template_mapped: bool = Field(..., description="Asserts template placeholder variables resolved")
    recipient_data: RecipientChannelContract = Field(..., description="Attached validated recipient reference")

class RoutingDispatchContract(BaseModel):
    routing_policy: Dict[str, Any] = Field(..., description="Routing and dispatch priority rules")
    routing_resolved: bool = Field(..., description="Asserts gateway routing parameters resolved")
    rendered_template: TemplateMappingContract = Field(..., description="Attached rendered template reference")

class QueueSchedulingContract(BaseModel):
    queue_details: Dict[str, Any] = Field(..., description="Dispatch queue names parameters")
    notification_enqueued: bool = Field(..., description="Asserts payload successfully appended to queues")
    routing: RoutingDispatchContract = Field(..., description="Attached routing policy reference")

class DeliveryExecutionContract(BaseModel):
    dispatch_outcome: Dict[str, Any] = Field(..., description="Gateway transmission response results")
    delivery_executed: bool = Field(..., description="Asserts transmission execution triggered")
    enqueued: QueueSchedulingContract = Field(..., description="Attached enqueued details reference")

class DeliveryValidationContract(BaseModel):
    audit_outcome: Dict[str, Any] = Field(..., description="Dispatch audit validation report results")
    delivery_validated: bool = Field(..., description="Asserts dispatch outcome is validated successfully")
    dispatched: DeliveryExecutionContract = Field(..., description="Attached execution details reference")

class NotificationMetadataContract(BaseModel):
    notification_identifier: str = Field(..., description="Unique notification identifier")
    lineage_step: str = Field(..., description="Lineage trace step")
    metadata_generated: bool = Field(..., description="Asserts audit metadata created")
    validated_delivery: DeliveryValidationContract = Field(..., description="Attached validated delivery reference")

class AcknowledgementContract(BaseModel):
    delivery_readiness_status: str = Field(..., description="Final delivery readiness status indicator")
    ack_recorded: bool = Field(..., description="Asserts success acknowledgement recorded")
    metadata: NotificationMetadataContract = Field(..., description="Attached metadata details reference")

class NotificationResponseContract(BaseModel):
    success: bool = Field(..., description="Indicates if notification execution was completed successfully")
    notification_identifier: str = Field(..., description="Unique dispatch reference identifier")
    delivery_status: str = Field(..., description="Status of delivery validation")
    assembled_metadata: Dict[str, Any] = Field(default_factory=dict, description="Audit logging meta info")
