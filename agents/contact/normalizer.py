import re
from urllib.parse import urlparse, urlunparse

class ContactNormalizer:
    @staticmethod
    def normalize_email(email: str) -> str:
        if not email:
            return ""
        return email.strip().lower()

    @staticmethod
    def normalize_phone(phone: str) -> str:
        if not phone:
            return ""
        cleaned = phone.strip()
        # Keep only digits and a potential leading plus
        has_plus = cleaned.startswith("+")
        digits = "".join(c for c in cleaned if c.isdigit())
        if not digits:
            return ""
        return f"+{digits}" if has_plus else digits

    @staticmethod
    def normalize_social(url: str) -> str:
        if not url:
            return ""
        cleaned = url.strip()
        
        # Add protocol if missing
        if not cleaned.startswith(("http://", "https://")):
            cleaned = "https://" + cleaned
            
        try:
            parsed = urlparse(cleaned)
            # Normalize scheme, hostname (lowercase), and path
            scheme = parsed.scheme.lower() if parsed.scheme else "https"
            netloc = parsed.netloc.lower() if parsed.netloc else ""
            path = parsed.path
            
            # Remove trailing slash in path if not root
            if path and path != "/" and path.endswith("/"):
                path = path[:-1]
                
            # Reconstruct URL without query parameters or fragments to keep it clean
            normalized = urlunparse((scheme, netloc, path, "", "", ""))
            return normalized
        except Exception:
            # Fallback to simple cleanup if urlparse fails
            cleaned = cleaned.rstrip("/")
            return cleaned
