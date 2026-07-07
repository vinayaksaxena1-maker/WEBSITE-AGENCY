import re

class ExportValidator:
    @staticmethod
    def scan_for_credentials(file_content: str) -> bool:
        """
        Scans file content to block leakage of API keys, tokens or secrets.
        Returns True if clean, False if credentials are found.
        """
        # Patterns matching api keys or database passwords
        patterns = [
            r"(?i)api[-_]?key\s*[:=]\s*['\"][a-zA-Z0-9]{20,}['\"]",
            r"(?i)password\s*[:=]\s*['\"][a-zA-Z0-9!@#$%^&*()_+]{8,}['\"]",
            r"(?i)secret[-_]?key\s*[:=]\s*['\"][a-zA-Z0-9+/]{20,}['\"]",
            r"(?i)aws[-_]?key"
        ]
        
        for p in patterns:
            if re.search(p, file_content):
                return False
        return True
