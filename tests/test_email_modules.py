import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.email.email_agent import EmailAgent
from agents.email.email_contracts import GeneratedEmailDraft
from agents.email.email_validator import EmailValidator

@pytest.mark.asyncio
async def test_pipeline_success():
    agent = EmailAgent()
    
    raw_inputs = {
        "lead_profile": {
            "domain": "https://www.fitsport.com",
            "niche": "Gym"
        },
        "audit_report": {
            "audit_score": 85,
            "mobile_score": 60,
            "speed_score": 80
        },
        "prototype_report": {
            "prototype_url": "https://cdn.upgradeagency.com/prototypes/fitsport/index.html"
        },
        "contact_info": {
            "name": "Jane Doe",
            "email": "JANE@FITSPORT.COM"
        }
    }
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": (
                                "Subject: Upgrade proposal for Fitsport - Redesign Redy\n\n"
                                "Hi Jane Doe,\n\n"
                                "We reviewed your website and noticed opportunities for mobile responsiveness optimization. "
                                "Our audit scored it at 85/100. We built a custom prototype with mobile viewport adapter at "
                                "https://cdn.upgradeagency.com/prototypes/fitsport/index.html for you.\n\n"
                                "Best regards,\nWebsite Agency"
                            )
                        }
                    ]
                }
            }
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    
    # Reset last call time to avoid real throttle delay during test run
    from agents.email.ai_generation_manager import AIGenerationManager
    AIGenerationManager._last_call_time = 0.0
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        res = await agent.generate_outreach_email(raw_inputs)
        
    assert res["success"] is True
    assert "final_package" in res
    
    final_pkg = res["final_package"]
    assert "email_payload" in final_pkg
    assert "metadata" in final_pkg
    
    payload = final_pkg["email_payload"]
    assert payload["subject"] == "Upgrade proposal for Fitsport - Redesign Redy"
    assert "mobile responsiveness optimization" in payload["text_body"]
    assert "fitsport/index.html" in payload["html_body"]
    # Verify Context Builder normalization (lowercase email, stripped domain protocol)
    assert payload["target_email"] == "jane@fitsport.com"
    
    meta = final_pkg["metadata"]
    assert "execution_id" in meta
    assert meta["validation_status"] == "PASS"

@pytest.mark.asyncio
async def test_missing_mandatory_input():
    agent = EmailAgent()
    
    # Missing contact_info
    raw_inputs = {
        "lead_profile": {
            "domain": "fitsport.com",
            "niche": "Gym"
        },
        "audit_report": {
            "audit_score": 85,
            "mobile_score": 60,
            "speed_score": 80
        },
        "prototype_report": {
            "prototype_url": "https://cdn.upgradeagency.com/prototypes/fitsport/index.html"
        }
    }
    
    res = await agent.generate_outreach_email(raw_inputs)
    
    assert res["success"] is False
    assert "Mandatory upstream data missing" in res["error"]

@pytest.mark.asyncio
async def test_validation_failure_with_placeholders():
    bad_draft = GeneratedEmailDraft(
        subject="Hello [Name]",
        body="Your score is {audit_score}",
        target_email="test@test.com"
    )
    
    with pytest.raises(ValueError) as exc:
        EmailValidator.validate_draft(bad_draft)
        
    assert "Email validation failed" in str(exc.value)
    assert "unresolved placeholders" in str(exc.value)
