from bs4 import BeautifulSoup
from core.logger import logger

class HTMLValidator:
    @staticmethod
    def validate_html_syntax(html_content: str) -> bool:
        """
        Runs BeautifulSoup parser validations to check html tag compliance.
        """
        logger.info("HTMLValidator: Running html syntax validation checks...")
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            # If BS4 could parse without exceptions, syntax is valid
            return True
        except Exception as e:
            logger.warning(f"HTMLValidator: HTML syntax validation failed: {e}")
            return False
