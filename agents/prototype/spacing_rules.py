from typing import Dict, Any

class SpacingRules:
    @staticmethod
    def get_spacing_rules(theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deduces structural paddings, margins, and gaps rules from theme presets tokens.
        """
        theme_tokens = theme.get("tokens", {})
        spacing_tokens = theme_tokens.get("spacing", {})
        
        # Build rules defaults
        base = spacing_tokens.get("base_unit", "4px")
        section_padding = spacing_tokens.get("section_padding", "64px 0")
        grid_gap = spacing_tokens.get("gap_md", "16px")

        return {
            "section_padding": section_padding,
            "element_margin_bottom": "1.5rem",
            "grid_gap": grid_gap,
            "container_max_width": "1200px",
            "line_height_multiplier": 1.6
        }
