from typing import Dict, Any

class SpacingScaler:
    @staticmethod
    def get_scaled_gap(base_gap: int, device: str) -> int:
        """
        Calculates grid layout gaps scaling factor.
        """
        if device in ["Mobile", "Small Mobile"]:
            return max(8, int(base_gap * 0.5))
        elif device in ["Mobile Large", "Tablet"]:
            return max(12, int(base_gap * 0.75))
        return base_gap
