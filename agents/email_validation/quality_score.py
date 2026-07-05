class QualityScoreCalculator:
    GENERIC_DOMAINS = {
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com",
        "icloud.com", "zoho.com", "protonmail.com", "yandex.com", "gmx.com",
        "mail.com", "live.com", "msn.com", "comcast.net", "sbcglobal.net"
    }

    @staticmethod
    def is_generic_domain(domain: str) -> bool:
        if not domain:
            return False
        return domain.strip().lower() in QualityScoreCalculator.GENERIC_DOMAINS

    @staticmethod
    def calculate(
        email: str,
        is_syntax_valid: bool,
        is_dns_valid: bool,
        is_mx_valid: bool,
        is_disposable: bool,
        is_role_based: bool,
        website_domain: str = ""
    ) -> int:
        """
        Calculates the quality score from 0 to 100.
        """
        if not is_syntax_valid or is_disposable:
            return 0
            
        if not is_dns_valid or not is_mx_valid:
            return 30
            
        # Extract email domain
        email_clean = email.strip().lower()
        parts = email_clean.split("@")
        if len(parts) != 2:
            return 0
        email_domain = parts[1]
        
        # Clean website domain for comparison
        web_clean = website_domain.strip().lower()
        # Remove http/https and path/query
        web_clean = web_clean.replace("https://", "").replace("http://", "").split("/")[0].replace("www.", "")
        
        # Role email takes precedence in reducing score
        if is_role_based:
            return 60
            
        # Match checks
        if email_domain == web_clean:
            return 100  # Perfect match
            
        if QualityScoreCalculator.is_generic_domain(email_domain):
            return 80  # Verified Generic
            
        return 90  # Business Email (different domain or domain alias)
