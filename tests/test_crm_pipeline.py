import pytest
from pydantic import ValidationError
from agents.crm.crm_contracts import CRMExecutionPackageContract
from agents.crm.input_manager import InputManager
from agents.crm.crm_context_builder import CRMContextBuilder
from agents.crm.relationship_manager import RelationshipManager
from agents.crm.lifecycle_manager import LifecycleManager
from agents.crm.output_validator import OutputValidator
from agents.crm.package_formatter import PackageFormatter
from agents.crm.metadata_generator import MetadataGenerator
from agents.crm.crm_agent import CRMAgent

@pytest.fixture
def valid_followup_package():
    return {
        "formatted_followup_package": {
            "workflow_information": {
                "workflow_id": "WF-999-XYZ",
                "email_ref": "EXEC-EM-999",
                "execution_ref": "EX-WF-999",
                "validation_summary": {"overall_result": "VALID"},
                "processing_summary": {"processing_status": "COMPLETED"},
                "configuration_summary": {
                    "workflow_config": {"auto_start": True},
                    "agency_config": {"sender_name": "AI Agency", "sender_email": "agent@agency.com"},
                    "brand_voice_config": {"tone": "Formal"},
                    "followup_config": {"max_retries": 3, "delay_days": 2}
                },
                "workflow_context": {"lead_id": "LEAD-123"},
                "followup_context": {
                    "recipient_email": "owner@store.com",
                    "subject": "Urgent proposal upgrade"
                }
            },
            "sequence_information": {
                "sequence_id": "SEQ-999",
                "workflow_id": "WF-999-XYZ",
                "sequence_definition": {"name": "Follow-Up Sequence"},
                "sequence_stages": [{"stage_number": 1, "delay_interval_days": 2}],
                "sequence_metadata": {"sequence_version": "1.0"},
                "processing_context": {}
            },
            "state_information": {
                "workflow_state": {"workflow_id": "WF-999-XYZ", "lifecycle_state": "ACTIVE"},
                "processing_state": {"processing_id": "PROC-SEQ-999", "processing_status": "INITIALIZED"},
                "validation_state": {"validation_status": "COMPLETED"},
                "publication_state": {"publication_status": "PUBLISHED"},
                "state_metadata": {"state_timestamp": "2026-07-06T02:00:00Z"}
            },
            "validation_information": {"overall_validation_result": "VALID"},
            "processing_information": {"processing_status": "COMPLETED"},
            "packaging_status": "COMPLETED"
        },
        "metadata_package": {
            "execution_id": "EXEC-FO-999",
            "engine_version": "FOLLOWUP-1.0",
            "contract_version": "1.0",
            "processing_timestamp": "2026-07-06T02:00:00Z",
            "validation_timestamp": "2026-07-06T02:00:00Z",
            "processing_status": "COMPLETED",
            "validation_status": "PASSED"
        },
        "validation_report": {"overall_validation_result": "VALID"},
        "processing_status": "COMPLETED"
    }

@pytest.fixture
def valid_crm_inputs(valid_followup_package):
    return {
        "followup_execution_package": valid_followup_package,
        "crm_config": {
            "sync_enabled": True,
            "auto_promote": True
        },
        "workflow_config": {
            "sync_enabled": False
        },
        "agency_config": {
            "sender_name": "Web Upgrade Agency"
        },
        "brand_voice_config": {
            "tone": "Casual"
        }
    }

def test_input_acquisition(valid_crm_inputs):
    inputs = InputManager.load_inputs(valid_crm_inputs)
    assert inputs.followup_execution_package.processing_status == "COMPLETED"
    assert inputs.crm_config["sync_enabled"] is True

def test_crm_context_assembly_and_duplicate_resolution(valid_crm_inputs):
    inputs = InputManager.load_inputs(valid_crm_inputs)
    context = CRMContextBuilder.build_context(inputs)
    
    assert context.crm_id.startswith("CRM-")
    assert context.workflow_id == "WF-999-XYZ"
    
    # Priority check: crm_config sync_enabled is True, overriding workflow_config False
    assert context.crm_context["crm_configuration"]["sync_enabled"] is True
    assert context.crm_context["crm_processing_rules"]["sync_enabled"] is True

def test_relationship_creation(valid_crm_inputs):
    inputs = InputManager.load_inputs(valid_crm_inputs)
    context = CRMContextBuilder.build_context(inputs)
    relationship = RelationshipManager.create_relationship(context)
    
    assert relationship.crm_id == context.crm_id
    assert relationship.relationship_id.startswith("REL-")
    assert relationship.customer_references["customer_email"] == "owner@store.com"
    assert relationship.customer_references["followup_reference"] == "EXEC-FO-999"

def test_lifecycle_initialization(valid_crm_inputs):
    inputs = InputManager.load_inputs(valid_crm_inputs)
    context = CRMContextBuilder.build_context(inputs)
    relationship = RelationshipManager.create_relationship(context)
    lifecycle = LifecycleManager.initialize_lifecycle(relationship)
    
    assert lifecycle.lifecycle_state["current_lifecycle_status"] == "PROSPECT"
    assert lifecycle.relationship_state["current_relationship_status"] == "ACTIVE"
    assert lifecycle.workflow_state["workflow_identifier"] == "WF-999-XYZ"

def test_output_validation_rules(valid_crm_inputs):
    inputs = InputManager.load_inputs(valid_crm_inputs)
    context = CRMContextBuilder.build_context(inputs)
    relationship = RelationshipManager.create_relationship(context)
    lifecycle = LifecycleManager.initialize_lifecycle(relationship)
    
    validated = OutputValidator.validate_package(context, relationship, lifecycle)
    assert validated.validation_status == "PASSED"
    assert validated.validation_identifier.startswith("VAL-CRM-")
    
    # Validation failure: mismatch crm_id
    relationship.crm_id = "CRM-MISMATCH"
    with pytest.raises(ValueError, match="Relationship crm_id does not match context crm_id"):
        OutputValidator.validate_package(context, relationship, lifecycle)

@pytest.mark.asyncio
async def test_end_to_end_crm_agent(valid_crm_inputs):
    agent = CRMAgent()
    result = await agent.execute_crm(valid_crm_inputs)
    
    assert result["success"] is True
    final_pkg = result["final_package"]
    assert final_pkg["processing_status"] == "COMPLETED"
    assert final_pkg["metadata_package"]["engine_version"] == "CRM-1.0"
    
    # Structural schema checks
    crm_pkg = CRMExecutionPackageContract(**final_pkg)
    assert crm_pkg.metadata_package.validation_status == "PASSED"
    assert crm_pkg.formatted_crm_package["packaging_status"] == "COMPLETED"
