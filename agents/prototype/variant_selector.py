from typing import Dict, Any
from core.logger import logger

class VariantSelector:
    @staticmethod
    def select_variant(component_name: str, theme: Dict[str, Any]) -> str:
        """
        Maps component to style presets based on design theme.
        """
        category = theme.get("category", "Modern Business").lower()

        if "luxury" in category:
            return "luxury"
        elif "marketing" in category or "studio" in category:
            return "creative"
        elif "medical" in category:
            return "medical"
        elif "technology" in category:
            return "tech-minimal"

        return "modern-business"
