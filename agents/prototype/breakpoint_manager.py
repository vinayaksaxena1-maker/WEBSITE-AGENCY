from typing import Dict, Any

class BreakpointManager:
    @staticmethod
    def get_breakpoints() -> Dict[str, Dict[str, Any]]:
        """
        Returns the standard configurable screen size viewports boundaries mapping matrix.
        """
        return {
            "Desktop XL": {"min_width": 1440, "container_width": 1360, "grid_columns": 12},
            "Desktop": {"min_width": 1280, "container_width": 1200, "grid_columns": 12},
            "Laptop": {"min_width": 1024, "container_width": 960, "grid_columns": 12},
            "Tablet": {"min_width": 768, "container_width": 720, "grid_columns": 6},
            "Mobile Large": {"min_width": 480, "container_width": 440, "grid_columns": 4},
            "Mobile": {"min_width": 360, "container_width": 340, "grid_columns": 2},
            "Small Mobile": {"min_width": 0, "container_width": 300, "grid_columns": 1}
        }
