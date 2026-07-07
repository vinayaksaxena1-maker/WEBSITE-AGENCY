from bs4 import BeautifulSoup
from core.logger import logger

class BuildOptimizer:
    @staticmethod
    def validate_html_size(html_content: str) -> int:
        """
        Calculates and checks HTML file size output to prevent buffer size overflow warnings.
        """
        size_bytes = len(html_content.encode("utf-8"))
        if size_bytes > 500000:
            logger.warning(f"BuildOptimizer: FinOps warning: Compiled HTML size is {size_bytes} bytes (exceeds 500KB benchmark).")
        return size_bytes
