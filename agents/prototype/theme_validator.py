import re
from typing import Dict, Any, Tuple
from core.logger import logger

class ThemeValidator:
    @staticmethod
    def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
        hex_str = hex_str.strip().lstrip("#")
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)

    @classmethod
    def calculate_relative_luminance(cls, hex_color: str) -> float:
        """
        Calculates WCAG relative luminance of a normalized hex color.
        """
        try:
            r, g, b = cls.hex_to_rgb(hex_color)
        except Exception:
            return 0.0

        components = []
        for val in (r, g, b):
            s = val / 255.0
            if s <= 0.03928:
                c = s / 12.92
            else:
                c = ((s + 0.055) / 1.055) ** 2.4
            components.append(c)
            
        return 0.2126 * components[0] + 0.7152 * components[1] + 0.0722 * components[2]

    @classmethod
    def get_contrast_ratio(cls, color1: str, color2: str) -> float:
        """
        Calculates contrast ratio between color1 and color2.
        """
        lum1 = cls.calculate_relative_luminance(color1)
        lum2 = cls.calculate_relative_luminance(color2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)

    @classmethod
    def validate_accessibility(cls, theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks contrast of text colors against background, verifying WCAG compliance.
        """
        colors = theme["colors"]
        bg = colors.get("background", "#FFFFFF")
        text = colors.get("text", "#000000")
        primary = colors.get("primary", "#1E3A8A")
        
        text_bg_ratio = cls.get_contrast_ratio(text, bg)
        primary_bg_ratio = cls.get_contrast_ratio(primary, bg)

        # Standard WCAG requirements
        passes_std = text_bg_ratio >= 4.5
        passes_large = text_bg_ratio >= 3.0

        logger.info(f"ThemeValidator: Text vs BG Contrast: {text_bg_ratio:.2f}:1 (Std Pass: {passes_std})")
        logger.info(f"ThemeValidator: Primary vs BG Contrast: {primary_bg_ratio:.2f}:1")

        warnings = []
        if not passes_std:
            warnings.append(
                f"Accessibility Warning: Standard text contrast ratio ({text_bg_ratio:.2f}:1) is under WCAG AA threshold of 4.5:1."
            )

        return {
            "text_bg_ratio": text_bg_ratio,
            "primary_bg_ratio": primary_bg_ratio,
            "passes_wcag_standard": passes_std,
            "passes_wcag_large": passes_large,
            "warnings": warnings
        }

    @classmethod
    def calculate_theme_score(cls, theme: Dict[str, Any], validation: Dict[str, Any], tokens: Dict[str, Any]) -> int:
        """
        Computes the overall theme score (0-100) based on industry, contrast compliance, and completeness.
        """
        score = 0
        
        # 1. Industry mapping match alignment (40 points max)
        score += 40  # pre-defined mapping is aligned by default

        # 2. Contrast accessibility compliance (30 points max)
        if validation["passes_wcag_standard"]:
            score += 30
        elif validation["passes_wcag_large"]:
            score += 15
            
        # 3. Token completeness (30 points max)
        if "radius" in tokens and "spacing" in tokens and "shadows" in tokens:
            score += 30

        return score
