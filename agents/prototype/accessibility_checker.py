from bs4 import BeautifulSoup

class AccessibilityChecker:
    @staticmethod
    def audit_accessibility(html_content: str) -> int:
        """
        Calculates accessibility scores checking ARIA landmarks and elements.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        score = 100
        
        # Check nav landmark role
        if not soup.find("nav"):
            score -= 15
        elif not soup.find("nav").get("aria-label"):
            score -= 10
            
        # Check img alt descriptions
        imgs = soup.find_all("img")
        for img in imgs:
            if not img.get("alt"):
                score -= 10
                
        return max(50, score)
