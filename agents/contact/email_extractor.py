import re
from typing import List, Set

class EmailExtractor:
    # Regex to find email addresses in raw text
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    # Regex to find mailto links in HTML
    MAILTO_PATTERN = re.compile(r'href=["\']mailto:([^?\'"\s>]+)', re.IGNORECASE)

    def extract(self, html_content: str) -> List[str]:
        if not html_content:
            return []
            
        emails: Set[str] = set()
        
        # 1. Extract from mailto hrefs
        for match in self.MAILTO_PATTERN.finditer(html_content):
            email = match.group(1).strip()
            if email:
                emails.add(email)
                
        # 2. Extract from raw text
        # Remove script and style blocks first to prevent extracting fake emails or JS strings
        clean_html = re.sub(r'<(script|style)\b[^>]*>([\s\S]*?)</\1>', '', html_content, flags=re.IGNORECASE)
        for match in self.EMAIL_PATTERN.finditer(clean_html):
            emails.add(match.group(0).strip())
            
        # Clean and filter duplicates
        result = []
        for email in emails:
            # Simple check to filter out common false positives (like image placeholders)
            if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                result.append(email)
                
        return sorted(result)
