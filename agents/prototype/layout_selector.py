from typing import Dict, Any

class LayoutSelector:
    @staticmethod
    def select_layout_type(niche: str) -> str:
        """
        Determines the optimal layout preset type based on the industry niche.
        """
        n_lower = niche.strip().lower()
        if "portfolio" in n_lower or "photography" in n_lower:
            return "portfolio-layout"
        elif "shop" in n_lower or "e-commerce" in n_lower:
            return "e-commerce-grid"
        elif "blog" in n_lower or "magazine" in n_lower:
            return "editorial-flow"
        elif "landing" in n_lower or "promo" in n_lower:
            return "landing-page"
        
        return "one-page-app"
