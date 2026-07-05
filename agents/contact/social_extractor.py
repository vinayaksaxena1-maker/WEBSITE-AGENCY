import re
from typing import Dict, List, Set
from urllib.parse import urlparse

class SocialExtractor:
    # Regex to find links (href attributes) in HTML
    HREF_PATTERN = re.compile(r'href=["\'](https?://[^"\']+|//[^"\']+|[^"\']+)["\']', re.IGNORECASE)

    # Platforms and their matching regex patterns/substrings
    PLATFORM_PATTERNS = {
        "facebook": re.compile(r'(?:facebook\.com|fb\.com)', re.IGNORECASE),
        "instagram": re.compile(r'instagram\.com', re.IGNORECASE),
        "linkedin": re.compile(r'linkedin\.com', re.IGNORECASE),
        "twitter": re.compile(r'(?:twitter\.com|x\.com)', re.IGNORECASE),
        "youtube": re.compile(r'(?:youtube\.com|youtu\.be)', re.IGNORECASE),
        "whatsapp": re.compile(r'(?:wa\.me|api\.whatsapp\.com|whatsapp\.com/send)', re.IGNORECASE),
        "google_business": re.compile(r'(?:google\.com/maps|g\.page|maps\.google\.com)', re.IGNORECASE),
    }

    def extract(self, html_content: str, base_url: str = "") -> Dict[str, List[str]]:
        extracted: Dict[str, Set[str]] = {platform: set() for platform in self.PLATFORM_PATTERNS}
        
        if not html_content:
            return {platform: [] for platform in self.PLATFORM_PATTERNS}

        # Find all hrefs
        for match in self.HREF_PATTERN.finditer(html_content):
            url = match.group(1).strip()
            
            # Format protocol-relative URLs
            if url.startswith("//"):
                url = "https:" + url
                
            for platform, pattern in self.PLATFORM_PATTERNS.items():
                if pattern.search(url):
                    # For google maps / wa.me, we keep it as is. For others, we make sure it's absolute
                    if not url.startswith(("http://", "https://")):
                        # Avoid treating paths as absolute URLs for social media unless they match pattern
                        continue
                    extracted[platform].add(url)
                    
        return {platform: sorted(list(urls)) for platform, urls in extracted.items()}
