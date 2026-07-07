class PerformanceChecker:
    @staticmethod
    def audit_performance(html_content: str) -> int:
        """
        Determines speed scoring matching build file sizes parameters.
        """
        size_bytes = len(html_content.encode("utf-8"))
        if size_bytes > 500000:
            return 80
        return 100
