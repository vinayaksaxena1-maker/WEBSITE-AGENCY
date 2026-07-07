from typing import Dict, Any
from core.logger import logger
from agents.prototype.theme_library import get_theme_preset

class ThemeSelector:
    @staticmethod
    def select_theme(niche: str, visuals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deduce optimal design system parameters from niche and visual intelligence inputs.
        Preserves custom primary colors if detected by visual analyzer to preserve identity.
        """
        logger.info(f"ThemeSelector: Selecting visual theme for category '{niche}'...")
        
        # 1. Fetch library preset matching niche
        preset = get_theme_preset(niche)
        
        # Deep copy to prevent mutating library objects
        theme = {
            "name": preset["name"],
            "category": preset["category"],
            "personality": preset["personality"],
            "colors": preset["colors"].copy(),
            "typography": preset["typography"].copy()
        }

        # 2. Preserve visual identity check:
        # If visual analyzer detected a valid primary color, merge it to sustain branding continuity
        v_primary = visuals.get("primary_color")
        if v_primary and v_primary.startswith("#") and v_primary.upper() not in ("#FFFFFF", "#000000"):
            logger.info(f"ThemeSelector: Merging existing visual primary color: '{v_primary}'")
            theme["colors"]["primary"] = v_primary.upper()
            
        v_secondary = visuals.get("secondary_color")
        if v_secondary and v_secondary.startswith("#") and v_secondary.upper() not in ("#FFFFFF", "#000000"):
            theme["colors"]["secondary"] = v_secondary.upper()

        logger.info(f"ThemeSelector: Selected theme '{theme['name']}' successfully.")
        return theme
