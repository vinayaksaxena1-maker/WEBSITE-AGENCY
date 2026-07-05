from bs4 import BeautifulSoup, Tag
from typing import Dict, Any, List

class SemanticDetector:
    @staticmethod
    def detect_semantic_elements(soup: BeautifulSoup) -> Dict[str, List[str]]:
        """
        Scans the cleaned DOM for HTML5 semantic tags and groups them by type.
        """
        semantic_tags = ["header", "nav", "main", "section", "article", "aside", "footer", "form", "button"]
        matches = {tag: [] for tag in semantic_tags}

        for tag in soup.find_all(True):
            name = tag.name.lower()
            if name in matches:
                # Store node descriptive selector (id, class, or tag tag-path)
                id_val = tag.get("id")
                class_val = " ".join(tag.get("class", []))
                desc = f"{name}"
                if id_val:
                    desc += f"#{id_val}"
                elif class_val:
                    desc += f".{class_val.replace(' ', '.')}"
                matches[name].append(desc)

        return matches
