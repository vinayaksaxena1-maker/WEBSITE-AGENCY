import re
from bs4 import BeautifulSoup, Comment
from core.logger import logger

class DOMParser:
    @staticmethod
    def parse_and_clean(html_content: str) -> BeautifulSoup:
        """
        Parses raw HTML and removes scripts, styles, tracking codes, ads,
        comments, and hidden nodes. Normalizes whitespace.
        """
        logger.info("DOMParser: Commencing raw HTML preprocessing and cleanup...")
        
        if not html_content:
            return BeautifulSoup("<html><body></body></html>", "html.parser")

        # Parse using standard bs4 html parser
        soup = BeautifulSoup(html_content, "html.parser")

        # 1. Remove scripts, styles, iframe, and noscript tags
        for tag in soup(["script", "style", "noscript", "iframe"]):
            tag.decompose()

        # 2. Remove comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # 3. Remove known trackers, ads, and hidden elements by class/id matching
        tracker_pattern = re.compile(
            r"analytics|tracker|ad-wrapper|banner-ad|google-tag|gtm|fb-pixel|hidden|display-none",
            re.IGNORECASE
        )
        
        for element in soup.find_all(True):
            # Check ID
            elem_id = element.get("id", "")
            if elem_id and tracker_pattern.search(elem_id):
                element.decompose()
                continue

            # Check Classes
            elem_classes = element.get("class", [])
            if elem_classes:
                classes_str = " ".join(elem_classes)
                if tracker_pattern.search(classes_str):
                    element.decompose()
                    continue

            # Check style attribute for display:none or visibility:hidden
            style_attr = element.get("style", "")
            if style_attr and ("display:none" in style_attr.replace(" ", "") or "visibility:hidden" in style_attr.replace(" ", "")):
                element.decompose()

        logger.info("DOMParser: DOM preprocessing and normalization completed successfully.")
        return soup
