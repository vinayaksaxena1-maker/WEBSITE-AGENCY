from typing import Dict, Any

class TypographyScaler:
    @staticmethod
    def get_scaled_font(base_font_size: int, device: str) -> int:
        """
        Scales base font sizes down depending on device size to avoid layout overflows.
        """
        # Base font scale: H1 size e.g. 36px on Desktop, scales down on Mobile
        if device in ["Mobile", "Small Mobile"]:
            return int(base_font_size * 0.7)
        elif device in ["Mobile Large", "Tablet"]:
            return int(base_font_size * 0.85)
        return base_font_size
