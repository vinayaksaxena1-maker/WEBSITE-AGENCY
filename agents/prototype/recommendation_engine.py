from typing import Dict, List

class RecommendationEngine:
    @staticmethod
    def get_recommendations(metrics: Dict[str, int]) -> tuple[List[str], List[str]]:
        """
        Calculates improvement recommendations and warning logs based on score values.
        """
        recs = []
        warns = []
        
        if metrics.get("html", 100) < 100:
            recs.append("Fine-tune CTA hover transition")
        if metrics.get("performance", 100) < 100:
            recs.append("Optimize SVG background assets size")
            warns.append("Prototype build size exceeds typical weight thresholds.")
        if metrics.get("accessibility", 100) < 100:
            recs.append("Ensure contrast ratios pass AA levels")
            
        return recs, warns
