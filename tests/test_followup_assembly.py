import pytest
from pydantic import ValidationError
from agents.followup.followup_contracts import UnifiedInputContract, WorkflowContextContract
from agents.followup.input_manager import InputManager
from agents.followup.workflow_builder import WorkflowBuilder
from agents.followup.followup_agent import FollowUpAgent

@pytest.fixture
def valid_raw_inputs():
    return {
        "final_email_package": {
            "email_payload": {
                "subject": "Upgrade your dental website",
                "html_body": "<html><body>Hello Dr. Smith</body></html>",
                "text_body": "Hello Dr. Smith",
                "target_email": "dentist@local.com"
            },
            "metadata": {
                "execution_id": "EXEC-12345",
                "engine_version": "EMAIL-1.0",
                "validation_status": "PASSED",
                "validation_report": {
                    "validation_id": "VAL-987",
                    "status": "VALID",
                    "checked_at": "2026-07-06T00:00:00Z",
                    "structural_validation": "PASS",
                    "personalization_validation": "PASS",
                    "communication_validation": "PASS",
                    "factual_validation": "PASS",
                    "formatting_validation": "PASS",
                    "overall_validation_result": "VALID"
                },
                "processing_metadata": {
                    "processing_timestamp": "2026-07-06T00:00:00Z",
                    "processing_status": "COMPLETED",
                    "execution_duration_sec": 1.5,
                    "completion_status": "SUCCESS"
                },
                "publication_metadata": {
                    "publication_status": "PUBLISHED",
                    "publication_timestamp": "2026-07-06T00:00:00Z",
                    "output_package_identifier": "PKG-001"
                }
            }
        },
        "followup_config": {
            "max_retries": 3,
            "delay_days": 2
        },
        "workflow_config": {
            "auto_start": True
        },
        "agency_config": {
            "sender_name": "AI Agency",
            "sender_email": "agent@agency.com"
        },
        "brand_voice_config": {
            "tone": "Professional"
        }
    }

def test_input_manager_validation(valid_raw_inputs):
    # Test valid input loading
    contract = InputManager.load_inputs(valid_raw_inputs)
    assert isinstance(contract, UnifiedInputContract)
    assert contract.final_email_package.metadata.execution_id == "EXEC-12345"
    assert contract.followup_config["max_retries"] == 3

    # Test missing mandatory key raises ValueError
    invalid_inputs = valid_raw_inputs.copy()
    del invalid_inputs["followup_config"]
    with pytest.raises(ValueError, match="Input acquisition failed"):
        InputManager.load_inputs(invalid_inputs)

def test_workflow_builder_context_consolidation(valid_raw_inputs):
    input_contract = InputManager.load_inputs(valid_raw_inputs)
    context = WorkflowBuilder.build_context(input_contract)
    
    assert isinstance(context, WorkflowContextContract)
    assert context.email_ref == "EXEC-12345"
    assert context.workflow_id.startswith("WF-")
    assert context.execution_ref.startswith("EX-WF-")
    assert context.validation_summary["overall_result"] == "VALID"
    assert context.processing_summary["processing_status"] == "COMPLETED"
    
    # Verify duplicate resolution / consolidation of configs
    assert context.configuration_summary["workflow_config"]["auto_start"] is True
    assert context.configuration_summary["agency_config"]["sender_name"] == "AI Agency"
    assert context.configuration_summary["agency_config"]["completion_status"] == "SUCCESS"

@pytest.mark.asyncio
async def test_followup_agent_orchestration(valid_raw_inputs):
    agent = FollowUpAgent()
    result = await agent.execute_followup(valid_raw_inputs)
    
    assert result["success"] is True
    assert "final_package" in result
    assert result["final_package"]["formatted_followup_package"]["workflow_information"]["email_ref"] == "EXEC-12345"

    # Test failure propagation
    invalid_inputs = valid_raw_inputs.copy()
    del invalid_inputs["final_email_package"]
    result_fail = await agent.execute_followup(invalid_inputs)
    assert result_fail["success"] is False
    assert "Input acquisition failed" in result_fail["error"]
