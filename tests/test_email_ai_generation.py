import pytest
import time
from unittest.mock import AsyncMock, MagicMock, patch
from agents.email.email_contracts import AIPromptPackage
from agents.email.ai_generation_manager import AIGenerationManager
from config.config import settings

@pytest.mark.asyncio
async def test_ai_generation_mock_response():
    original_key = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = "mock_key_for_testing"
    
    prompt = AIPromptPackage(
        prompt_subject="Default Subject",
        prompt_body="Default Body",
        target_email="test@business.com",
        variables={"compiled_prompt": "Hello AI"}
    )
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "Subject: New Redesign Redy\nDear Owner,\nWe upgraded your page."
                        }
                    ]
                }
            }
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        AIGenerationManager._last_call_time = 0.0
        
        draft = await AIGenerationManager.generate_email(prompt)
        
        assert draft.subject == "New Redesign Redy"
        assert "Dear Owner," in draft.body
        assert draft.target_email == "test@business.com"
        
        mock_post.assert_called_once()
        called_url = mock_post.call_args[0][0]
        assert "gemini-3.5-flash" in called_url
        assert "key=mock_key_for_testing" in called_url

    settings.GEMINI_API_KEY = original_key

@pytest.mark.asyncio
async def test_throttling_delay():
    original_key = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = "mock_key_for_testing"
    
    prompt = AIPromptPackage(
        prompt_subject="Subject",
        prompt_body="Body",
        target_email="test@business.com",
        variables={}
    )
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Subject: Test\nBody: Hello"}]}}]
    }
    mock_resp.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        with patch("asyncio.sleep") as mock_sleep:
            current_time = time.time()
            AIGenerationManager._last_call_time = current_time - 4.0
            
            await AIGenerationManager.generate_email(prompt)
            
            mock_sleep.assert_called_once()
            slept_duration = mock_sleep.call_args[0][0]
            assert 7.5 <= slept_duration <= 8.5

    settings.GEMINI_API_KEY = original_key
