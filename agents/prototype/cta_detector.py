from bs4 import BeautifulSoup
from typing import List, Dict, Any

class CTADetector:
    @staticmethod
    def detect_ctas(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Locates call-to-actions, buttons, WhatsApp hooks, and registration links.
        """
        ctas = []
        
        # Targets: buttons and anchors with button-like classes or action patterns
        elements = soup.find_all(["button", "a"])
        
        for element in elements:
            text = element.get_text().strip()
            if not text:
                continue
                
            href = element.get("href", "")
            classes = " ".join(element.get("class", [])).lower()
            tag_name = element.name.lower()
            
            is_cta = False
            priority = "secondary"
            cta_type = "button"
            
            # Identify CTAs
            if tag_name == "button":
                is_cta = True
                priority = "primary" if "primary" in classes or "btn-main" in classes or "btn-submit" in classes else "secondary"
            elif tag_name == "a":
                # Check specific url type first
                if any(x in href.lower() for x in ["wa.me", "api.whatsapp.com"]):
                    is_cta = True
                    cta_type = "whatsapp"
                    priority = "primary"
                elif href.startswith("tel:"):
                    is_cta = True
                    cta_type = "call"
                    priority = "primary"
                elif any(x in classes for x in ["btn", "button", "cta", "signup", "login", "register"]):
                    is_cta = True
                    priority = "primary" if "primary" in classes or "main" in classes else "secondary"
                elif any(x in text.lower() for x in ["book", "reserve", "register", "contact", "pricing"]):
                    is_cta = True
                    priority = "primary"

            if is_cta:
                ctas.append({
                    "text": text[:50],
                    "href": href,
                    "type": cta_type,
                    "priority": priority
                })

        return ctas
