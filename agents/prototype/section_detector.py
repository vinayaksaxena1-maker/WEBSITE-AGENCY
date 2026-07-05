from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any

class SectionDetector:
    @staticmethod
    def detect_sections(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Scans block tags (sections, articles, main divs) to identify page sections
        and categorize them logically (Hero, Services, Contact, etc.).
        """
        sections = []
        # Find structural blocks
        blocks = soup.find_all(["section", "article", "header", "footer"])
        
        # Fallback to top-level divs if no section tags exist
        if not blocks:
            body = soup.find("body")
            if body:
                blocks = [c for c in body.children if isinstance(c, Tag) and c.name.lower() == "div"]

        for idx, block in enumerate(blocks):
            block_id = block.get("id", f"section-{idx}")
            block_class = " ".join(block.get("class", [])).lower()
            text_content = block.get_text().lower()
            
            # Default category
            category = "general"
            
            # Rule matches
            if block.name.lower() == "header" or "header" in block_class:
                category = "header"
            elif block.name.lower() == "footer" or "footer" in block_class:
                category = "footer"
            elif "hero" in block_class or "jumbotron" in block_class or "banner" in block_class:
                category = "hero"
            elif "service" in block_class or "feature" in block_class or "product" in block_class:
                category = "services"
            elif "pricing" in block_class or "plan" in block_class:
                category = "pricing"
            elif "about" in block_class or "team" in block_class or "who" in block_class:
                category = "about"
            elif "contact" in block_class or "map" in block_class or "form" in block_class:
                category = "contact"
            elif "faq" in block_class or "accordion" in block_class or "question" in block_class:
                category = "faq"
            elif "testimonial" in block_class or "review" in block_class or "feedback" in block_class:
                category = "testimonials"

            sections.append({
                "id": block_id,
                "category": category,
                "element": block.name,
                "text_snippet": block.get_text()[:60].strip().replace("\n", " ") + "..."
            })
            
        return sections
