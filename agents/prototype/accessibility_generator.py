import re

class AccessibilityGenerator:
    @staticmethod
    def enrich_accessibility(html_content: str) -> str:
        """
        Adds ARIA attributes (roles, labels) to interactive landmarks.
        """
        # Ensure navigation links have proper aria landmarks
        enriched = html_content
        enriched = re.sub(
            r"<nav([^>]*)>",
            r'<nav\1 aria-label="Main Navigation" role="navigation">',
            enriched
        )
        enriched = re.sub(
            r"<header([^>]*)>",
            r'<header\1 role="banner">',
            enriched
        )
        enriched = re.sub(
            r"<footer([^>]*)>",
            r'<footer\1 role="contentinfo">',
            enriched
        )
        return enriched
