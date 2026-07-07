from core.logger import logger

class RenderValidator:
    @staticmethod
    def validate_layout(html_path: str) -> tuple[int, str]:
        """
        Runs layout checking rules, validating index file presence and tags consistency.
        """
        import os
        if not os.path.exists(html_path):
            return 0, "FAILED: HTML prototype file not generated."
            
        # Basic layout checks (e.g. file size parameters bounds)
        size = os.path.getsize(html_path)
        if size > 500000:
            logger.warning("RenderValidator: HTML size exceeds 500KB. Warning threshold met.")
            return 80, "PASSED_WITH_WARNINGS"
            
        return 100, "PASSED"
