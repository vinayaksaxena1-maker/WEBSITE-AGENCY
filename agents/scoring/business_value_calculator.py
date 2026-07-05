from typing import Any
from agents.scoring.interfaces import IBusinessValueCalculator

class BusinessValueCalculator(IBusinessValueCalculator):
    def __init__(self):
        self.industry_multipliers = {
            "Hospital": 1.5,
            "Clinic": 1.5,
            "Hotel": 1.5,
            "Law Firm": 1.5,
            "Real Estate": 1.5,
            "Restaurant": 1.2,
            "Gym": 1.2,
            "Travel": 1.2,
            "Business": 1.2,
            "Corporate": 1.2,
            "School": 1.0,
            "Education": 1.0,
            "NGO": 1.0,
            "Publisher": 0.8,
            "Portfolio": 0.8
        }

    def calculate_business_value_index(
        self, 
        audit: Any, 
        business_profile: Any, 
        lead_score: int
    ) -> float:
        # Fail-safe defaults if records are missing
        if not audit:
            # High default audit_score to represent minimum deficiency
            audit_score = 100
            trust_score = 0
        else:
            audit_score = getattr(audit, "audit_score", 100)
            trust_score = getattr(audit, "trust_score", 0)

        if not business_profile:
            industry = "Unknown"
            confidence = 0.50
        else:
            industry = getattr(business_profile, "industry", "Unknown")
            confidence = getattr(business_profile, "confidence", 1.0)

        # 1. Website Deficiencies Factor
        deficiencies = (100.0 - audit_score) / 100.0
        # Deficiencies must not be negative
        deficiencies = max(0.0, deficiencies)

        # 2. Niche Confidence Factor
        niche_confidence = max(0.0, min(1.0, confidence))

        # 3. Industry Multiplier
        industry_mult = self.industry_multipliers.get(industry, 1.0)

        # 4. Contact Multiplier
        contact_mult = 1.2 if trust_score >= 50 else 0.8

        # 5. Lead Score Factor
        lead_score_factor = lead_score / 100.0

        # Multi-dimensional calculation
        bvi = deficiencies * niche_confidence * industry_mult * contact_mult * lead_score_factor
        return round(float(bvi), 4)
