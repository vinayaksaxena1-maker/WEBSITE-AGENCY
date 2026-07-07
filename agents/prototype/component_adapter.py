from typing import Dict, Any

class ComponentAdapter:
    @staticmethod
    def adapt_card_layout(device: str) -> str:
        """
        Determines grid layout configurations for component lists cards.
        """
        if device in ["Mobile", "Small Mobile"]:
            return "flex flex-col gap-4"
        elif device == "Tablet":
            return "grid grid-cols-2 gap-6"
        return "grid grid-cols-3 gap-8"
