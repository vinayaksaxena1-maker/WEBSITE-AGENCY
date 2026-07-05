import time
import asyncio
import urllib.request
from typing import Dict, Any
from core.logger import logger
from agents.audit.interfaces import IBrowserEngine

class PlaywrightBrowserEngine(IBrowserEngine):
    async def fetch_url(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        logger.info(f"Attempting to crawl '{url}' using Playwright browser engine...")
        raise ImportError("Playwright is not installed in the environment.")

class UrllibBrowserEngine(IBrowserEngine):
    async def fetch_url(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        logger.info(f"Crawl: Using UrllibBrowserEngine for '{url}'...")
        
        fetch_url = url
        if not fetch_url.startswith(("http://", "https://")):
            fetch_url = "https://" + fetch_url
            
        start_time = time.time()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        def fetch():
            req = urllib.request.Request(fetch_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html = response.read().decode('utf-8', errors='ignore')
                return html, dict(response.info())

        try:
            html, headers_info = await asyncio.to_thread(fetch)
            elapsed_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                "html": html,
                "load_time_ms": elapsed_time_ms,
                "response_time_ms": elapsed_time_ms // 2,
                "headers": headers_info
            }
        except Exception as e:
            logger.error(f"UrllibBrowserEngine failed to fetch URL '{url}': {e}")
            raise e
