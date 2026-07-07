from typing import Dict, Any, List

class ResponsiveRules:
    @staticmethod
    def get_container_widths() -> Dict[str, str]:
        """
        Returns Tailwind class equivalents for container widths.
        """
        return {
            "Desktop XL": "max-w-7xl mx-auto px-6",
            "Desktop": "max-w-6xl mx-auto px-6",
            "Laptop": "max-w-5xl mx-auto px-6",
            "Tablet": "max-w-3xl mx-auto px-4",
            "Mobile Large": "max-w-xl mx-auto px-4",
            "Mobile": "w-full px-4",
            "Small Mobile": "w-full px-2"
        }
