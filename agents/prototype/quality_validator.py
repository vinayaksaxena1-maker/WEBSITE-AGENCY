from bs4 import BeautifulSoup

class QualityValidator:
    @staticmethod
    def check_html_syntax(html_content: str) -> int:
        """
        Parses HTML content, returning score (0-100) based on parsing syntax success.
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            if not soup.find("html"):
                return 50
            return 100
        except Exception:
            return 0
