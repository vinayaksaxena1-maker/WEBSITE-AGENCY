from typing import Dict, Any

class GridAdapter:
    @staticmethod
    def adapt_grid(columns: int, device: str) -> int:
        """
        Collapses column grid allocations according to device size constraints.
        """
        if device in ["Mobile", "Small Mobile"]:
            return 1
        elif device == "Mobile Large":
            return min(2, columns)
        elif device == "Tablet":
            return min(6, columns if columns % 2 == 0 or columns == 1 else columns - 1)
        return columns
