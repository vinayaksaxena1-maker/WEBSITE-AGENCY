from bs4 import BeautifulSoup
from typing import Dict, Any, List
from agents.prototype.dom_classifier import DOMClassifier

class ComponentMapper:
    @staticmethod
    def map_components(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Walks the DOM to extract component positions, styles, tags, and parent definitions.
        """
        components = []
        
        # We classify and map elements with specific semantic tag configurations
        elements = soup.find_all(True)
        for idx, tag in enumerate(elements):
            ctype = DOMClassifier.classify_node(tag)
            
            # Skip container tags from generic element list to keep map focused
            if ctype in ["container", "element"] and tag.name.lower() in ["div", "span", "p", "html", "body"]:
                continue

            # Identify parents
            parent_tag = tag.parent
            parent_id = "root"
            if parent_tag and parent_tag.name:
                parent_id = f"{parent_tag.name}#{parent_tag.get('id', '')}" if parent_tag.get('id') else parent_tag.name

            components.append({
                "id": f"{tag.name}-{idx}",
                "type": ctype,
                "tag": tag.name,
                "parent": parent_id,
                "classes": tag.get("class", []),
                "text_snippet": tag.get_text()[:40].strip()
            })

        return components
