import re
from typing import List, Set

class PhoneExtractor:
    # Regex to find tel: hrefs in HTML
    TEL_PATTERN = re.compile(r'href=["\']tel:([^?\'"\s>]+)', re.IGNORECASE)
    
    # Standard phone regex to find numbers in text
    # e.g., matches +1 (123) 456-7890, +44 20 7946 0958, 080-1234-5678, etc.
    PHONE_PATTERN = re.compile(
        r'(?:\+?\d{1,4}[-.\s]?)?\(?\d{2,5}\)?[-.\s]?\d{2,5}[-.\s]?\d{3,9}'
    )

    def extract(self, html_content: str) -> List[str]:
        if not html_content:
            return []
            
        phones: Set[str] = set()
        
        # 1. Extract from tel hrefs
        for match in self.TEL_PATTERN.finditer(html_content):
            phone = match.group(1).strip()
            if phone:
                # Remove common URL encoded components
                phone = re.sub(r'%20', '', phone)
                phones.add(phone)
                
        # 2. Extract from raw text (exclude script/style tags)
        clean_html = re.sub(r'<(script|style)\b[^>]*>([\s\S]*?)</\1>', '', html_content, flags=re.IGNORECASE)
        # Strip HTML tags entirely to search raw text content
        text_content = re.sub(r'<[^>]+>', ' ', clean_html)
        
        for match in self.PHONE_PATTERN.finditer(text_content):
            num = match.group(0).strip()
            # Clean and keep only numbers and plus sign
            cleaned = "".join(c for c in num if c.isdigit() or c == "+")
            # Limit search to realistic phone lengths (7 to 15 digits)
            digit_count = sum(c.isdigit() for c in cleaned)
            if 7 <= digit_count <= 15:
                phones.add(num)
                
        return sorted(list(phones))
