from bs4 import BeautifulSoup
from typing import Dict, Any

class LayoutAnalyzer:
    @staticmethod
    def analyze_layout(soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Analyzes DOM tag configurations to determine core layout schemes (Bento, grids, columns).
        """
        layout_type = "single-column"
        container_width = "fixed"
        
        # Count main structure structures
        div_classes = []
        for div in soup.find_all("div"):
            c = " ".join(div.get("class", []))
            if c:
                div_classes.append(c.lower())
                
        div_classes_str = " ".join(div_classes)
        
        # Grid/Flex detection
        has_grid = "grid" in div_classes_str or "col-" in div_classes_str
        has_flex = "flex" in div_classes_str or "d-flex" in div_classes_str
        
        # 1. Classify layouts
        if "bento" in div_classes_str:
            layout_type = "bento-grid"
        elif has_grid and ("col-md-4" in div_classes_str or "col-lg-3" in div_classes_str):
            layout_type = "three-column-grid"
        elif has_grid and "col-md-6" in div_classes_str:
            layout_type = "two-column-split"
        elif has_flex and "flex-row" in div_classes_str:
            layout_type = "flex-row-layout"
        elif has_grid:
            layout_type = "multi-column-grid"

        # 2. Container sizing
        if "fluid" in div_classes_str or "w-100" in div_classes_str:
            container_width = "full-width"

        return {
            "layout_type": layout_type,
            "container_width": container_width,
            "has_grid": has_grid,
            "has_flex": has_flex
        }
