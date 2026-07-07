from bs4 import BeautifulSoup

class SEOChecker:
    @staticmethod
    def audit_seo(html_content: str) -> int:
        """
        Audits meta descriptions and title header parameters.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        score = 100
        
        if not soup.find("title"):
            score -= 30
        if not soup.find("meta", attrs={"name": "description"}):
            score -= 30
        if not soup.find("link", attrs={"rel": "canonical"}):
            score -= 20
            
        return max(40, score)
