from typing import Dict, Tuple

class DeviceRenderer:
    @staticmethod
    def get_viewports() -> Dict[str, Tuple[int, int]]:
        """
        Returns resolutions matrices for viewports capture.
        """
        return {
            "desktop": (1440, 900),
            "laptop": (1024, 768),
            "tablet": (768, 1024),
            "mobile": (375, 812)
        }
