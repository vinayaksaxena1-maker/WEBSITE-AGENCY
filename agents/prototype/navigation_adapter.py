from typing import Dict, Any

class NavigationAdapter:
    @staticmethod
    def get_navigation_style(device: str) -> str:
        """
        Determines navigation styling adaptation types (horizontal navbar or mobile hamburger drawer).
        """
        if device in ["Desktop XL", "Desktop", "Laptop"]:
            return "horizontal-navbar"
        return "hamburger-drawer"
