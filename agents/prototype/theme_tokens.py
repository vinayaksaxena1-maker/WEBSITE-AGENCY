from typing import Dict, Any

class ThemeTokens:
    @staticmethod
    def compile_tokens(theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compiles layout sizes, spacing scales, border radius metrics,
        elevations, and animations properties into design tokens.
        """
        category = theme.get("category", "Modern Business").lower()

        # 1. Spacing System Scale
        spacing = {
            "base_unit": "4px",
            "gap_sm": "8px",
            "gap_md": "16px",
            "gap_lg": "24px",
            "section_padding": "64px 0",
            "container_width": "1200px"
        }

        # 2. Typography Font Sizes Scale (Major Second scale base 16px)
        typography = {
            "font_size_h1": "2.5rem",   # 40px
            "font_size_h2": "2.0rem",   # 32px
            "font_size_h3": "1.75rem",  # 28px
            "font_size_body": "1rem",   # 16px
            "font_size_sm": "0.875rem", # 14px
            "line_height_heading": "1.2",
            "line_height_body": "1.6"
        }

        # 3. Border radius tokens (e.g. Modern presets use pill, traditional use sharp)
        if "medical" in category or "studio" in category:
            radius = {
                "button": "24px",  # Rounded Pill style
                "card": "12px",
                "input": "8px"
            }
        elif "luxury" in category or "corporate" in category:
            radius = {
                "button": "4px",   # Traditional Sleek
                "card": "6px",
                "input": "4px"
            }
        else:
            radius = {
                "button": "8px",   # Standard Modern
                "card": "8px",
                "input": "6px"
            }

        # 4. Box Shadow Elevation System
        shadows = {
            "elevation_0": "none",
            "elevation_1": "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)",
            "elevation_2": "0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)",
            "elevation_3": "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)"
        }

        # 5. Animation Profiles
        animations = {
            "transition_speed": "0.2s",
            "transition_easing": "cubic-bezier(0.4, 0, 0.2, 1)",
            "hover_scale": "scale(1.02)",
            "hover_brightness": "brightness(0.95)"
        }

        return {
            "spacing": spacing,
            "typography": typography,
            "radius": radius,
            "shadows": shadows,
            "animations": animations
        }
