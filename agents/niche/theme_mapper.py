from agents.niche.interfaces import IThemeMapper

class ThemeMapper(IThemeMapper):
    def __init__(self):
        # Maps specific industries to layout theme templates
        self.theme_map = {
            "Hospital": "clinical_comfort",
            "Clinic": "clinical_comfort",
            "School": "academic_prestige",
            "Education": "academic_prestige",
            "Gym": "energy_dynamic",
            "Restaurant": "luxury_hospitality",
            "Hotel": "luxury_hospitality",
            "Law Firm": "justice_executive",
            "Real Estate": "urban_estate",
            "NGO": "impact_trust",
            "Publisher": "corporate_edge",
            "Business": "corporate_edge",
            "Corporate": "corporate_edge",
            "Portfolio": "creative_showcase",
            "Travel": "wanderlust_adventure"
        }

    def recommend_theme(self, industry: str) -> str:
        # Defaults to corporate_edge if the industry cannot be mapped
        return self.theme_map.get(industry, "corporate_edge")
