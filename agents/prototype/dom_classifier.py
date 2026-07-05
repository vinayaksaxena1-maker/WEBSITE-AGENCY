from bs4 import Tag
from typing import Dict, Any, List

class DOMClassifier:
    @staticmethod
    def classify_node(tag: Tag) -> str:
        """
        Classifies a BS4 tag into standard visual and functional component types.
        """
        tag_name = tag.name.lower()
        
        # 1. Semantic Tag Rules
        if tag_name == "header":
            return "header"
        if tag_name == "footer":
            return "footer"
        if tag_name == "nav":
            return "navigation"
        if tag_name == "form":
            return "form"
        if tag_name == "button" or (tag_name == "a" and "btn" in " ".join(tag.get("class", []))):
            return "cta"
        if tag_name in ("img", "picture", "figure"):
            return "image"
        if tag_name in ("video", "audio"):
            return "media"

        # 2. Class and Attribute Rules
        class_str = " ".join(tag.get("class", [])).lower()
        tag_id = tag.get("id", "").lower()
        
        if "card" in class_str or "grid-item" in class_str:
            return "card"
        if "hero" in class_str or "jumbotron" in class_str or "hero" in tag_id:
            return "hero"
        if "popup" in class_str or "modal" in class_str or "dialog" in class_str:
            return "modal"
        if "tab" in class_str:
            return "tabs"
        if "accordion" in class_str or "collapse" in class_str:
            return "accordion"
            
        return "container" if tag_name in ("div", "section", "article", "main", "aside") else "element"
