import re
from urllib.parse import urlparse
from core.logger import logger

class DomainFilter:
    def __init__(self):
        # List of common directory, search engine, and social media platforms to filter out
        self.blacklist = [
            "facebook.com", "twitter.com", "instagram.com", "linkedin.com", "youtube.com",
            "yelp.com", "wikipedia.org", "yellowpages.com", "tripadvisor.com", "pinterest.com",
            "reddit.com", "github.com", "medium.com", "tumblr.com", "vimeo.com", "google.com",
            "yahoo.com", "bing.com", "duckduckgo.com", "baidu.com", "yandex.com", "tiktok.com"
        ]
        
        # Validation regex for standard internet domains
        self.domain_regex = re.compile(
            r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$",
            re.IGNORECASE
        )

    def normalize_url(self, url: str) -> str:
        """
        Normalizes a URL to its root domain.
        Example: https://sub.domain.co.uk/page -> domain.co.uk
        """
        if not url:
            return ""
            
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        try:
            parsed = urlparse(url)
            netloc = parsed.netloc.lower()
            
            if ":" in netloc:
                netloc = netloc.split(":")[0]
                
            if netloc.startswith("www."):
                netloc = netloc[4:]
                
            return netloc
        except Exception as e:
            logger.debug(f"Failed to parse URL '{url}': {e}")
            return ""

    def is_valid_domain(self, domain: str) -> bool:
        """
        Checks if the domain matches valid formatting and is not local loopback.
        """
        if not domain:
            return False
            
        if domain in ["localhost", "127.0.0.1", "0.0.0.0"]:
            return False
            
        return bool(self.domain_regex.match(domain))

    def is_blacklisted(self, domain: str) -> bool:
        """
        Verifies if the domain belongs to a blacklisted directory or platform.
        """
        if not domain:
            return True
            
        for item in self.blacklist:
            if domain == item or domain.endswith("." + item):
                return True
        return False

    def validate(self, url: str) -> str:
        """
        Applies parsing and filter rules. Returns normalized domain if clean, else empty string.
        """
        normalized = self.normalize_url(url)
        if not self.is_valid_domain(normalized):
            return ""
        if self.is_blacklisted(normalized):
            return ""
        return normalized

domain_filter = DomainFilter()
