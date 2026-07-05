class RoleDetector:
    # Common role-based prefixes
    ROLE_PREFIXES = {
        "info",
        "support",
        "sales",
        "contact",
        "admin",
        "office",
        "hello",
        "careers",
        "jobs",
        "marketing",
        "billing",
        "help",
        "team",
        "feedback",
        "press",
        "media",
        "hr",
        "service"
    }

    @staticmethod
    def is_role_based(email: str) -> bool:
        if not email:
            return False
            
        parts = email.strip().lower().split("@")
        if not parts:
            return False
            
        local_part = parts[0]
        return local_part in RoleDetector.ROLE_PREFIXES
