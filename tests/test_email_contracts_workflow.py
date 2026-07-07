import pytest
from unittest.mock import patch
from pydantic import ValidationError
from agents.email.email_contracts import AuditReportContract, UnifiedInputPackage
from agents.email.context_builder import ContextBuilder
from agents.email.input_manager import InputManager
from agents.email.email_agent import EmailAgent

def test_pydantic_schema_validation_failures():
    # Audit scores must be in range [0, 100]
    with pytest.raises(ValidationError):
        AuditReportContract(audit_score=150, mobile_score=80, speed_score=90)
        
    with pytest.raises(ValidationError):
        AuditReportContract(audit_score=50, mobile_score=-10, speed_score=90)

def test_context_normalization_and_protocol_stripping():
    raw_inputs = {
        "lead_profile": {
            "domain": "   HTTPS://WWW.EXAMPLE-BUSINESS.COM/   ",
            "niche": "   Dental Practice   "
        },
        "audit_report": {
            "audit_score": 90,
            "mobile_score": 95,
            "speed_score": 85
        },
        "prototype_report": {
            "prototype_url": "   https://prototype.com/example/index.html   "
        },
        "contact_info": {
            "name": "   Dr. John Smith   ",
            "email": "   CONTACT@EXAMPLE-BUSINESS.COM   "
        }
    }
    
    # 1. InputManager loads inputs
    input_pkg = InputManager.load_inputs(raw_inputs)
    
    # 2. ContextBuilder builds context
    context = ContextBuilder.build_context(input_pkg)
    
    # Assertions on normalization rules
    assert context.target_domain == "example-business.com/"
    assert context.target_niche == "Dental Practice"
    assert context.target_email == "contact@example-business.com"
    assert context.contact_name == "Dr. John Smith"
    assert context.prototype_url == "https://prototype.com/example/index.html"
    assert context.speed_score == 85

@pytest.mark.asyncio
async def test_workflow_sequential_state_checking():
    agent = EmailAgent()
    
    raw_inputs = {
        "lead_profile": {
            "domain": "valid.com",
            "niche": "Law Firm"
        },
        "audit_report": {
            "audit_score": 92,
            "mobile_score": 94,
            "speed_score": 85
        },
        "prototype_report": {
            "prototype_url": "http://proto.com"
        },
        "contact_info": {
            "name": "John",
            "email": "john@valid.com"
        }
    }
    
    # Mock AIGenerationManager to throw an Exception and verify fail-fast error propagation
    with patch("agents.email.ai_generation_manager.AIGenerationManager.generate_email", side_effect=RuntimeError("AI generation failed unexpectedly")):
        res = await agent.generate_outreach_email(raw_inputs)
        assert res["success"] is False
        assert "AI generation failed unexpectedly" in res["error"]
