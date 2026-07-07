import re
import colorsys
from typing import Dict

# Basic mapping for standard HTML names
HTML_COLOR_MAP: Dict[str, str] = {
    "red": "#FF0000",
    "green": "#008000",
    "blue": "#0000FF",
    "black": "#000000",
    "white": "#FFFFFF",
    "gray": "#808080",
    "yellow": "#FFFF00",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "silver": "#C0C0C0",
    "maroon": "#800000",
    "olive": "#808000",
    "purple": "#800080",
    "teal": "#008080",
    "navy": "#000080",
    "orange": "#FFA500"
}

class ColorNormalizer:
    @staticmethod
    def normalize_color(color_str: str, fallback: str = "#FFFFFF") -> str:
        """
        Converts diverse color styles (RGB, RGBA, HSL, Hex name) into normalized HEX #RRGGBB.
        """
        if not color_str:
            return fallback

        color_str = color_str.strip().lower()

        # 1. Match Hex representation
        if color_str.startswith("#"):
            hex_val = color_str[1:]
            if len(hex_val) == 3:
                # Expand short hex: e.g. #1e3 -> #11EE33
                return "#" + "".join(c * 2 for c in hex_val).upper()
            elif len(hex_val) == 6 or len(hex_val) == 8:
                # Standard or hex with alpha: drop alpha if 8
                return "#" + hex_val[:6].upper()
            return fallback

        # 2. Match standard HTML color names
        if color_str in HTML_COLOR_MAP:
            return HTML_COLOR_MAP[color_str].upper()

        # 3. Match RGB/RGBA formats
        rgb_match = re.match(r"^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*[\d\.]+)?\s*\)$", color_str)
        if rgb_match:
            try:
                r = int(rgb_match.group(1))
                g = int(rgb_match.group(2))
                b = int(rgb_match.group(3))
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    return f"#{r:02x}{g:02x}{b:02x}".upper()
            except ValueError:
                pass
            return fallback

        # 4. Match HSL format: hsl(h, s%, l%)
        hsl_match = re.match(r"^hsl\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)$", color_str)
        if hsl_match:
            try:
                h = int(hsl_match.group(1)) / 360.0
                s = int(hsl_match.group(2)) / 100.0
                l = int(hsl_match.group(3)) / 100.0
                if 0 <= h <= 1 and 0 <= s <= 1 and 0 <= l <= 1:
                    r, g, b = colorsys.hls_to_rgb(h, l, s)
                    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}".upper()
            except ValueError:
                pass
            return fallback

        return fallback
