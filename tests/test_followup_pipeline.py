import pytest
from pydantic import ValidationError
from agents.followup.followup_contracts import FollowUpExecutionPackageContract
from agents.followup.input_manager import InputManager
from agents.followup.workflow_builder import WorkflowBuilder
from agents.followup.sequence_manager import SequenceManager
from agents.followup.state_manager import StateManager
from agents.followup.output_validator import OutputValidator
from agents.followup.package_formatter import PackageFormatter
from agents.followup.metadata_generator import MetadataGenerator
from agents.followup.followup_agent import FollowUpAgent

@pytest.fixture
def valid_inputs():
    return {
        "final_email_package": {
            "email_payload": {
                "subject": "Urgent upgrade required",
                "html_body": "<html><body>Hello</body></html>",
                "text_body": "Hello",
                "target_email": "owner@store.com"
            },
            "metadata": {
                "execution_id": "EXEC-EM-999",
                "engine_version": "EMAIL-1.0",
                "validation_status": "PASSED",
                "validation_report": {
                    "validation_id": "VAL-777",
                    "status": "VALID",
                    "checked_at": "2026-07-06T01:00:00Z",
                    "structural_validation": "PASS",
                    "personalization_validation": "PASS",
                    "communication_validation": "PASS",
                    "factual_validation": "PASS",
                    "formatting_validation": "PASS",
                    "overall_validation_result": "VALID"
                },
                "processing_metadata": {
                    "processing_timestamp": "2026-07-06T01:00:00Z",
                    "processing_status": "COMPLETED",
                    "execution_duration_sec": 0.8,
                    "completion_status": "SUCCESS"
                },
                "publication_metadata": {
                    "publication_status": "PUBLISHED",
                    "publication_timestamp": "2026-07-06T01:00:00Z",
                    "output_package_identifier": "PKG-999"
                }
            }
        },
        "followup_config": {
            "max_retries": 4,
            "delay_days": 3
        },
        "workflow_config": {
            "auto_start": True
        },
        "agency_config": {
            "sender_name": "Web Upgrade Agency",
            "sender_email": "outreach@agency.com"
        },
        "brand_voice_config": {
            "tone": "Casual"
        }
    }

def test_sequence_preparation(valid_inputs):
    inputs = InputManager.load_inputs(valid_inputs)
    context = WorkflowBuilder.build_context(inputs)
    sequence = SequenceManager.build_sequence(context)
    
    assert sequence.workflow_id == context.workflow_id
    assert sequence.sequence_id.startswith("SEQ-")
    assert len(sequence.sequence_stages) == 4
    assert sequence.sequence_stages[0]["delay_interval_days"] == 3
    assert sequence.sequence_stages[3]["delay_interval_days"] == 12

def test_state_initialization(valid_inputs):
    inputs = InputManager.load_inputs(valid_inputs)
    context = WorkflowBuilder.build_context(inputs)
    sequence = SequenceManager.build_sequence(context)
    state = StateManager.initialize_state(sequence)
    
    assert state.workflow_state["workflow_id"] == context.workflow_id
    assert state.workflow_state["current_status"] == "INITIALIZED"
    assert state.processing_state["processing_status"] == "INITIALIZED"
    assert state.validation_state["validation_status"] == "NOT_STARTED"
    assert state.publication_state["publication_status"] == "UNPUBLISHED"

def test_output_validation_logic(valid_inputs):
    inputs = InputManager.load_inputs(valid_inputs)
    context = WorkflowBuilder.build_context(inputs)
    sequence = SequenceManager.build_sequence(context)
    state = StateManager.initialize_state(sequence)
    
    # Validation passes for valid package
    validated = OutputValidator.validate_package(context, sequence, state)
    assert validated.validation_status == "PASSED"
    assert validated.approved_state["validation_state"]["validation_status"] == "COMPLETED"
    
    # Validation fails if sequence is empty
    sequence.sequence_stages = []
    with pytest.raises(ValueError, match="Sequence stages list is empty"):
        OutputValidator.validate_package(context, sequence, state)

@pytest.mark.asyncio
async def test_end_to_end_followup_agent(valid_inputs):
    agent = FollowUpAgent()
    result = await agent.execute_followup(valid_inputs)
    
    assert result["success"] is True
    final_pkg = result["final_package"]
    assert final_pkg["processing_status"] == "COMPLETED"
    assert final_pkg["metadata_package"]["engine_version"] == "FOLLOWUP-1.0"
    
    # Verify the output schema matches the Pydantic spec
    package_contract = FollowUpExecutionPackageContract(**final_pkg)
    assert package_contract.metadata_package.validation_status == "PASSED"
    assert package_contract.formatted_followup_package["packaging_status"] == "COMPLETED"
    assert package_contract.formatted_followup_package["state_information"]["publication_state"]["publication_status"] == "PUBLISHED"
