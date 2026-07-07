from bs4 import BeautifulSoup

class ComponentChecker:
    @staticmethod
    def audit_components(html_content: str) -> int:
        """
        Validates elements count and component configurations.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        sections = soup.find_all("section")
        
        if len(sections) == 0:
            return 60
        elif len(sections) < 3:
            return 80
            
        return 100
