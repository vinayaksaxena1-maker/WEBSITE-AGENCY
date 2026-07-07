from bs4 import BeautifulSoup

class UXChecker:
    @staticmethod
    def audit_ux(html_content: str) -> int:
        """
        Determines user flow usability.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        # Check standard sections presence (Header, Footer, CTA click triggers)
        score = 100
        if not soup.find("header"):
            score -= 30
        if not soup.find("footer"):
            score -= 30
        if not soup.find("button") and not soup.find("a", class_="btn"):
            score -= 20
            
        return max(50, score)
