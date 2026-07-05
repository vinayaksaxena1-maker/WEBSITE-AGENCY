from typing import Dict, Any, List

VIEWPORTS: Dict[str, Dict[str, int]] = {
    "desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1440, "height": 900},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844}
}

def get_viewport_profile(name: str) -> Dict[str, int]:
    if name not in VIEWPORTS:
        raise KeyError(f"Viewport profile '{name}' not configured.")
    return VIEWPORTS[name]

def list_viewport_profiles() -> List[str]:
    return list(VIEWPORTS.keys())
