import re
from urllib.parse import urlparse

class ContactValidator:
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")

    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return False
        return bool(ContactValidator.EMAIL_REGEX.match(email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        if not phone:
            return False
        # Clean whitespaces/dashes first
        cleaned = "".join(c for c in phone if c.isdigit() or c == "+")
        return bool(ContactValidator.PHONE_REGEX.match(cleaned))

    @staticmethod
    def validate_social(url: str, platform: str) -> bool:
        if not url:
            return False
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Map platform to expected keywords in domain name
            platform_keywords = {
                "facebook": ["facebook.com", "fb.com"],
                "instagram": ["instagram.com"],
                "linkedin": ["linkedin.com"],
                "twitter": ["twitter.com", "x.com"],
                "youtube": ["youtube.com", "youtu.be"],
                "whatsapp": ["wa.me", "whatsapp.com"],
            }
            
            keywords = platform_keywords.get(platform.lower(), [])
            return any(kw in domain for kw in keywords)
        except Exception:
            return False

    @staticmethod
    def determine_quality(contacts: dict) -> str:
        has_email = bool(contacts.get("primary_email"))
        has_phone = bool(contacts.get("phone"))
        
        social_fields = ["whatsapp", "facebook", "instagram", "linkedin", "twitter", "youtube"]
        has_social = any(bool(contacts.get(field)) for field in social_fields)
        
        if has_email and has_phone and has_social:
            return "Complete"
        elif has_email and not has_phone and not has_social:
            return "Email Only"
        elif not has_email and has_phone and not has_social:
            return "Phone Only"
        elif not has_email and not has_phone and has_social:
            return "Social Only"
        elif not has_email and not has_phone and not has_social:
            return "No Contact"
        else:
            return "Partial"
