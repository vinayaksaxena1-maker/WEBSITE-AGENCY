from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List

class IScoringCalculator(ABC):
    @abstractmethod
    def calculate_lead_score(self, audit_data: Any) -> Tuple[int, List[str]]:
        """
        Evaluates website deficiencies based on audit results.
        Returns a tuple of (lead_score: int, opportunities: List[str]).
        """
        pass

class IBusinessValueCalculator(ABC):
    @abstractmethod
    def calculate_business_value_index(
        self, 
        audit_data: Any, 
        business_profile_data: Any, 
        lead_score: int
    ) -> float:
        """
        Calculates the multi-dimensional Business Value Index (BVI).
        """
        pass

class IScoringAgent(ABC):
    @abstractmethod
    async def score_lead(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Main orchestration entry point:
        1. Verifies lead and fetches its Audit and BusinessProfile.
        2. Computes lead score using IScoringCalculator.
        3. Computes business value using IBusinessValueCalculator.
        4. Maps priority levels and AI processing decisions.
        5. Saves/updates scores in lead_scores table and updates lead status to SCORED.
        6. Enqueues task downstream to Redis contact_queue.
        7. Publishes 'lead_scored' event to Event Bus.
        """
        pass
