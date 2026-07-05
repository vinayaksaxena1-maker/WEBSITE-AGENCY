from typing import Dict, Any
from agents.audit.interfaces import IAuditRules
from agents.audit.scoring_strategies import (
    SeoScoreStrategy,
    MobileScoreStrategy,
    SpeedScoreStrategy,
    TrustScoreStrategy,
    DesignScoreStrategy
)

class AuditRules(IAuditRules):
    def __init__(self):
        self.schema_version = "1.0.0"
        self.audit_rule_version = "1.0.0"
        self.seo_strategy = SeoScoreStrategy()
        self.mobile_strategy = MobileScoreStrategy()
        self.speed_strategy = SpeedScoreStrategy()
        self.trust_strategy = TrustScoreStrategy()
        self.design_strategy = DesignScoreStrategy()

    def calculate_scores(self, parse_payload: Dict[str, Any]) -> Dict[str, Any]:
        seo_score = self.seo_strategy.evaluate(parse_payload)
        mobile_score = self.mobile_strategy.evaluate(parse_payload)
        speed_score = self.speed_strategy.evaluate(parse_payload)
        trust_score = self.trust_strategy.evaluate(parse_payload)
        design_score = self.design_strategy.evaluate(parse_payload)
        
        # Weighted score logic as defined in SDD-003 Section 12
        overall_score = int(
            0.25 * speed_score +
            0.20 * seo_score +
            0.20 * mobile_score +
            0.20 * trust_score +
            0.15 * design_score
        )
        
        summary_points = []
        if not parse_payload.get("ssl_valid", False):
            summary_points.append("SSL invalid/missing")
        if speed_score < 50:
            summary_points.append("poor page speed performance")
        if seo_score < 70:
            summary_points.append("SEO deficiencies (missing title/meta descriptions)")
        if mobile_score < 100:
            summary_points.append("non-responsive mobile viewport attributes")
            
        if not summary_points:
            summary = "Website is highly optimized with strong technical foundations."
        else:
            summary = f"Audit reveals key modernization opportunities: {', '.join(summary_points)}."
            
        return {
            "seo_score": seo_score,
            "mobile_score": mobile_score,
            "speed_score": speed_score,
            "trust_score": trust_score,
            "design_score": design_score,
            "audit_score": overall_score,
            "schema_version": self.schema_version,
            "audit_rule_version": self.audit_rule_version,
            "summary": summary
        }
