from typing import Tuple, List, Any
from agents.scoring.interfaces import IScoringCalculator

class ScoringCalculator(IScoringCalculator):
    def __init__(self):
        self.rules_version = "1.0.0"

    def calculate_lead_score(self, audit: Any) -> Tuple[int, List[str]]:
        if not audit:
            return 0, ["No audit data available"]
            
        score = 0
        opportunities = []

        # 1. Old Website Design (+30): design_score < 50
        if audit.design_score < 50:
            score += 30
            opportunities.append("Old Website Design")

        # 2. Mobile Responsiveness Issues (+25): mobile_score < 70
        if audit.mobile_score < 70:
            score += 25
            opportunities.append("Mobile Responsiveness Issues")

        # 3. Performance Problems (+20): speed_score < 60
        if audit.speed_score < 60:
            score += 20
            opportunities.append("Performance Problems")

        # 4. SEO Problems (+15): seo_score < 70
        if audit.seo_score < 70:
            score += 15
            opportunities.append("SEO Problems")

        # 5. Trust Issues (+10): trust_score < 70
        if audit.trust_score < 70:
            score += 10
            opportunities.append("Trust Issues")

        # 6. Broken Navigation (+10): seo_score < 50 or design_score < 40
        if audit.seo_score < 50 or audit.design_score < 40:
            score += 10
            opportunities.append("Broken Navigation")

        # 7. Poor CTA Placement (+10): design_score < 60
        if audit.design_score < 60:
            score += 10
            opportunities.append("Poor CTA Placement")

        # 8. Outdated Branding (+15): design_score < 50
        if audit.design_score < 50:
            score += 15
            opportunities.append("Outdated Branding")

        # 9. No SSL (+10): check summary or trust_score drop
        has_ssl_issue = False
        if audit.summary and "SSL invalid/missing" in audit.summary:
            has_ssl_issue = True
        elif audit.trust_score < 60:
            has_ssl_issue = True

        if has_ssl_issue:
            score += 10
            opportunities.append("No SSL")

        # 10. Accessibility Problems (+10): mobile_score < 80 or design_score < 80
        if audit.mobile_score < 80 or audit.design_score < 80:
            score += 10
            opportunities.append("Accessibility Problems")

        # Cap the score at 100
        lead_score = min(100, score)
        return lead_score, opportunities
