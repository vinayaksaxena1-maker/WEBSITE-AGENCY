import pytest
from agents.notification.notification_agent import NotificationAgent

@pytest.mark.asyncio
async def test_notification_workflow_success():
    agent = NotificationAgent()
    
    mock_request = {
        "request_identifier": "REQ-NOTIFY-999",
        "recipient_identifier": "john@doe.com",
        "notification_type": "EMAIL",
        "request_timestamp": "2026-07-07T00:00:00Z"
    }
    
    res = await agent.execute_notification(mock_request)
    assert res["success"] is True
    assert res["notification_identifier"].startswith("NOTIFY-")
    assert res["delivery_status"] == "READY"

@pytest.mark.asyncio
async def test_notification_workflow_precondition_failures():
    agent = NotificationAgent()
    
    # 1. Empty request payload
    res1 = await agent.execute_notification({})
    assert res1["success"] is False
    assert "cannot be empty" in res1["error"]
    
    # 2. Invalid request payload type
    res2 = await agent.execute_notification("not-a-dict") # type: ignore
    assert res2["success"] is False
    assert "must be a dictionary" in res2["error"]

@pytest.mark.asyncio
async def test_notification_workflow_invalid_recipient():
    agent = NotificationAgent()
    
    # Invalid email address pattern (no @)
    mock_request = {
        "request_identifier": "REQ-NOTIFY-999",
        "recipient_identifier": "invalid-email-address",
        "notification_type": "EMAIL",
        "request_timestamp": "2026-07-07T00:00:00Z"
    }
    
    res = await agent.execute_notification(mock_request)
    assert res["success"] is False
    assert "Recipient Validation failed" in res["error"]
