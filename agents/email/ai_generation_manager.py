import time
import asyncio
import httpx
from typing import Dict, Any
from config.config import settings
from core.logger import logger
from agents.email.email_contracts import AIPromptPackage, GeneratedEmailDraft

class AIGenerationManager:
    _last_call_time = 0.0
    _lock = asyncio.Lock()

    @classmethod
    async def generate_email(cls, prompt_package: AIPromptPackage) -> GeneratedEmailDraft:
        """
        Drafts the outreach email using the gemini-3.5-flash endpoint.
        Enforces a 12-second minimum delay between requests to remain under free tier limits.
        """
        api_key = settings.GEMINI_API_KEY
        
        async with cls._lock:
            current_time = time.time()
            elapsed = current_time - cls._last_call_time
            if elapsed < 12.0:
                delay = 12.0 - elapsed
                logger.info(f"AIGenerationManager Throttling: Delaying call by {delay:.2f} seconds to protect API rate limit.")
                await asyncio.sleep(delay)
                
            logger.info("AIGenerationManager: Executing API call to gemini-3.5-flash REST endpoint.")
            
            # If the key is dummy, return a default mock draft for verification / tests
            if api_key == "dummy_gemini_key":
                logger.warning("AIGenerationManager: Dummy Gemini key detected. Returning mock draft.")
                cls._last_call_time = time.time()
                return GeneratedEmailDraft(
                    subject=prompt_package.prompt_subject,
                    body=prompt_package.prompt_body,
                    target_email=prompt_package.target_email
                )
                
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt_package.variables.get("compiled_prompt", prompt_package.prompt_body)
                            }
                        ]
                    }
                ]
            }
            
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(endpoint, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Parse text content from response
                    text_output = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    
                    subject = prompt_package.prompt_subject
                    body = text_output
                    
                    # Parse subject line from text if formatted explicitly by AI
                    lines = text_output.split('\n')
                    if lines[0].lower().startswith("subject:"):
                        subject = lines[0][len("subject:"):].strip()
                        body = "\n".join(lines[1:]).strip()
                    elif lines[0].lower().startswith("subject line:"):
                        subject = lines[0][len("subject line:"):].strip()
                        body = "\n".join(lines[1:]).strip()
                        
                    cls._last_call_time = time.time()
                    return GeneratedEmailDraft(
                        subject=subject,
                        body=body,
                        target_email=prompt_package.target_email
                    )
            except Exception as e:
                logger.error(f"AIGenerationManager: API request failed: {e}", exc_info=True)
                raise RuntimeError(f"Failed to generate email via Gemini API: {e}")
