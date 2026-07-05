from bs4 import BeautifulSoup
from typing import Dict, Any, List

class NavigationDetector:
    @staticmethod
    def detect_navigation(soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Classifies page navigation structures and fetches navigation anchor labels.
        """
        nav_type = "unknown"
        links = []

        # Find navigation tags or standard class configurations
        nav_elements = soup.find_all(["nav", "header"])
        if not nav_elements:
            nav_elements = soup.find_all(class_=lambda c: c and any(x in c.lower() for x in ["nav", "menu", "navbar"]))

        for nav in nav_elements:
            classes = " ".join(nav.get("class", [])).lower()
            style = nav.get("style", "").lower()
            
            # Detect Nav Type
            if "sticky" in classes or "fixed" in classes or "fixed" in style or "sticky" in style:
                nav_type = "sticky-header"
            elif "hamburger" in classes or "mobile" in classes or soup.find(class_=lambda c: c and "hamburger" in c.lower()):
                nav_type = "hamburger-menu"
            elif "sidebar" in classes or "side" in classes:
                nav_type = "side-nav"
            elif "mega" in classes or "megamenu" in classes:
                nav_type = "mega-menu"
            elif nav_type == "unknown":
                nav_type = "standard-header"

            # Gather Anchor Links
            anchors = nav.find_all("a")
            for a in anchors:
                text = a.get_text().strip()
                if text and len(text) < 30 and text not in links:
                    links.append(text)

        # Fallback if no nav elements
        if not links:
            # Try to grab anchors from top level header list items
            header = soup.find("header")
            if header:
                for a in header.find_all("a"):
                    text = a.get_text().strip()
                    if text and len(text) < 30 and text not in links:
                        links.append(text)

        return {
            "type": nav_type,
            "links": links[:12]  # limit to top links
        }
