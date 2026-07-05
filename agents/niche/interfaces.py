from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class INicheClassifier(ABC):
    @abstractmethod
    def classify(self, html_content: str) -> Tuple[str, float]:
        """
        Classifies HTML content into one of the supported industries.
        Returns a tuple of (industry_name, confidence_score).
        """
        pass

class IThemeMapper(ABC):
    @abstractmethod
    def recommend_theme(self, industry: str) -> str:
        """
        Maps an industry name to a recommended design theme template.
        """
        pass

class INicheAgent(ABC):
    @abstractmethod
    async def detect_niche(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Main orchestration entry point:
        1. Checks lead status in database.
        2. Retrieves crawled page content/audited source.
        3. Classifies niche using hybrid rule & Gemini logics.
        4. Maps recommended theme.
        5. Saves profile to business_profiles and updates lead status to CLASSIFIED.
        6. Enqueues task downstream to Redis scoring_queue.
        7. Publishes 'niche_detected' event to Event Bus.
        """
        pass
