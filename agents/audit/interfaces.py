from abc import ABC, abstractmethod
from typing import Dict, Any

class IBrowserEngine(ABC):
    @abstractmethod
    async def fetch_url(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Launches the browser instance, loads the page, and extracts HTML & network statistics.
        
        Args:
            url: Target URL to fetch.
            timeout: Max fetch time in seconds.
            
        Returns:
            Dict containing:
                - "html": Raw HTML page source code string.
                - "load_time_ms": Duration to reach loaded state in ms.
                - "response_time_ms": Response start delay (TTFB) in ms.
                - "headers": Dict of HTTP response headers.
        """
        pass

class IAuditScoreStrategy(ABC):
    @abstractmethod
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        """
        Evaluates a specific category of web vitals/elements and returns a score out of 100.
        
        Args:
            page_data: Output dictionary containing parsed HTML source and timings.
            
        Returns:
            Integer score from 0 to 100.
        """
        pass

class IAuditAgent(ABC):
    @abstractmethod
    async def audit_site(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Runs the database checking, crawling, scoring, persistence,
        and downstream queue notification workflow.
        """
        pass

class IAuditService(ABC):
    @abstractmethod
    async def fetch_page_content(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Establishes socket SSL connections and invokes the browser abstraction engine.
        """
        pass

class IAuditRules(ABC):
    @abstractmethod
    def calculate_scores(self, parse_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates category scores using strategies, computes overall score, and generates a summary.
        """
        pass
