from typing import Dict, Any

class ContainerAdapter:
    @staticmethod
    def get_padding_rules(device: str) -> str:
        """
        Retrieves padding offsets depending on viewport size.
        """
        if device in ["Mobile", "Small Mobile"]:
            return "px-4 py-8"
        elif device in ["Mobile Large", "Tablet"]:
            return "px-6 py-12"
        return "px-8 py-16"
