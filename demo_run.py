import asyncio
from core.logger import logger
from core.health_monitor import health_monitor
from events.event_bus import event_bus
from agents.notification.notification_agent import NotificationAgent
from dashboard.dashboard import dashboard

async def sample_event_handler(data):
    logger.info(f"[HANDLER] Event handler caught data: {data}")

async def main():
    logger.info("=== STARTING AI WEBSITE UPGRADE AGENCY PIPELINE DEMO ===")
    
    # 1. System Health Check
    logger.info("Step 1: Inspecting System Health Status...")
    status = await health_monitor.check_health()
    logger.info(f"Database Connectivity: {status['database'].upper()}")
    logger.info(f"Redis Connectivity: {status['redis'].upper()}")
    
    # 2. Event Bus Subscription & Publishing
    logger.info("\nStep 2: Testing Decoupled Event Bus Messaging...")
    event_bus.subscribe("demo_event", sample_event_handler)
    await event_bus.publish("demo_event", {"message": "Hello from the EDK Pipeline!"})
    
    # 3. Notification Engine Execution
    logger.info("\nStep 3: Triggering Notification Agent Workflow...")
    notify_agent = NotificationAgent()
    mock_request = {
        "request_identifier": "REQ-NOTIFY-Demo101",
        "recipient_identifier": "user@testdomain.com",
        "notification_type": "EMAIL",
        "request_timestamp": "2026-07-07T00:00:00Z"
    }
    notify_result = await notify_agent.execute_notification(mock_request)
    logger.info(f"Notification Execution Result: {notify_result}")
    
    # 4. CLI Admin Dashboard Overview
    logger.info("\nStep 4: Rendering CLI Admin Dashboard...")
    await dashboard.render()
    
    logger.info("\n=== DEMO PIPELINE COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    asyncio.run(main())
