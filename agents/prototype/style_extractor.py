import re
from bs4 import BeautifulSoup
from collections import Counter
from typing import Dict, Any, Tuple
from agents.prototype.color_normalizer import ColorNormalizer

class StyleExtractor:
    @staticmethod
    def extract_styles(soup: BeautifulSoup) -> Tuple[Dict[str, str], str]:
        """
        Scans elements and inline style configs to extract primary, secondary,
        background, and text color configurations, and dominant font family.
        """
        bg_colors = []
        text_colors = []
        cta_colors = []
        font_families = []

        # 1. Scan inline style attributes on all tags
        for tag in soup.find_all(True):
            style_str = tag.get("style", "")
            if not style_str:
                continue

            # Parse colors
            bg_match = re.search(r"background(?:-color)?\s*:\s*([^;]+)", style_str, re.IGNORECASE)
            if bg_match:
                norm = ColorNormalizer.normalize_color(bg_match.group(1))
                bg_colors.append(norm)

            color_match = re.search(r"(?<!background-)color\s*:\s*([^;]+)", style_str, re.IGNORECASE)
            if color_match:
                norm = ColorNormalizer.normalize_color(color_match.group(1))
                if tag.name.lower() in ("button", "a"):
                    cta_colors.append(norm)
                else:
                    text_colors.append(norm)

            # Parse fonts
            font_match = re.search(r"font-family\s*:\s*([^;]+)", style_str, re.IGNORECASE)
            if font_match:
                font_name = font_match.group(1).replace("'", "").replace('"', "").split(",")[0].strip()
                font_families.append(font_name)

        # 2. Scan block elements or buttons classes to extract more CTA indications
        for tag in soup.find_all(["button", "a"]):
            classes = " ".join(tag.get("class", [])).lower()
            if "primary" in classes or "btn" in classes:
                # If there's an inline style or color, it's captured; otherwise simulate standard frequency weights
                pass

        # 3. Frequency resolution & fallbacks
        bg_counter = Counter(bg_colors)
        text_counter = Counter(text_colors)
        cta_counter = Counter(cta_colors)
        font_counter = Counter(font_families)

        # Resolved Background & Text Colors
        background_color = bg_counter.most_common(1)[0][0] if bg_colors else "#FFFFFF"
        text_color = text_counter.most_common(1)[0][0] if text_colors else "#000000"

        # Resolved Primary & Secondary theme Colors
        cta_most_common = cta_counter.most_common(2)
        if len(cta_most_common) >= 2:
            primary_color = cta_most_common[0][0]
            secondary_color = cta_most_common[1][0]
        elif len(cta_most_common) == 1:
            primary_color = cta_most_common[0][0]
            # Secondary is a fallback variation
            secondary_color = "#3B82F6" if primary_color != "#3B82F6" else "#1E3A8A"
        else:
            primary_color = "#1E3A8A"
            secondary_color = "#3B82F6"

        # Resolved Font Family
        font_family = font_counter.most_common(1)[0][0] if font_families else "sans-serif"

        resolved_colors = {
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "background_color": background_color,
            "text_color": text_color
        }

        return resolved_colors, font_family
