class ExportReport:
    @staticmethod
    def generate_report(version: str, size: int, checksum: str) -> str:
        """
        Formats export details summary markdown report.
        """
        return f"""# Prototype Export Package Report
## Version Tag: {version}
## Package File Size: {size} bytes
## Integrity Signature: {checksum}
## Status: COMPLETED
"""
