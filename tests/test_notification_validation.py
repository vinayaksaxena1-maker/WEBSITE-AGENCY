import pytest
from agents.notification.notification_managers import DeliveryValidationManager, NotificationMetadataManager

def test_notification_delivery_validation_success():
    dispatched = {
        "dispatch_outcome": {},
        "delivery_executed": True,
        "enqueued": {}
    }
    res = DeliveryValidationManager.validate_delivery(dispatched)
    assert res["delivery_validated"] is True
    assert res["audit_outcome"]["dispatch_verified"] is True

def test_notification_delivery_validation_failure():
    dispatched = {
        "dispatch_outcome": {},
        "delivery_executed": False,
        "enqueued": {}
    }
    with pytest.raises(ValueError, match="Dispatch execution outcome is missing"):
        DeliveryValidationManager.validate_delivery(dispatched)

def test_notification_metadata_generation():
    validated = {
        "audit_outcome": {},
        "delivery_validated": True,
        "dispatched": {}
    }
    res = NotificationMetadataManager.generate_metadata(validated)
    assert res["notification_identifier"].startswith("NOTIFY-")
    assert res["lineage_step"] == "notification_dispatch_lineage"
    assert res["metadata_generated"] is True
