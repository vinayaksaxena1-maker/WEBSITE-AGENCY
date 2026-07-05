class DisposableDetector:
    # Set of common disposable email domains
    DISPOSABLE_DOMAINS = {
        "mailinator.com",
        "10minutemail.com",
        "guerrillamail.com",
        "tempmail.com",
        "temp-mail.org",
        "yopmail.com",
        "dispostable.com",
        "maildrop.cc",
        "sharklasers.com",
        "guerrillamailblock.com",
        "guerrillamail.net",
        "guerrillamail.org",
        "guerrillamail.biz",
        "getairmail.com",
        "burnermail.io",
        "trashmail.com",
        "owlymail.com"
    }

    @staticmethod
    def is_disposable(domain: str) -> bool:
        if not domain:
            return False
        return domain.strip().lower() in DisposableDetector.DISPOSABLE_DOMAINS
