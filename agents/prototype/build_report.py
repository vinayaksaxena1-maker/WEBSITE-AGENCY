from typing import Dict, Any

class BuildReport:
    @staticmethod
    def generate_report(elapsed: float, size: int, count: int) -> str:
        """
        Formats compilation logs markdown reports.
        """
        return f"""# HTML Compilation Report
## Build Duration: {elapsed:.3f} seconds
## Output HTML Size: {size} bytes
## Components Compiled: {count}
"""
