import re

class SyntaxValidator:
    # Standard RFC compliant email regex
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    @staticmethod
    def validate(email: str) -> bool:
        if not email:
            return False
        
        email_clean = email.strip()
        
        # 1. Regex check
        if not SyntaxValidator.EMAIL_REGEX.match(email_clean):
            return False
            
        # 2. Extract parts
        parts = email_clean.split("@")
        if len(parts) != 2:
            return False
            
        local_part, domain_part = parts
        
        # 3. Check length constraints
        if len(email_clean) > 254:
            return False
        if len(local_part) > 64:
            return False
        if len(domain_part) > 255:
            return False
            
        # 4. Check domain TLD length (at least 2 characters)
        domain_parts = domain_part.split(".")
        if len(domain_parts) < 2:
            return False
        tld = domain_parts[-1]
        if len(tld) < 2:
            return False
            
        return True
