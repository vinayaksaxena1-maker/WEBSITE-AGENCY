class PreviewReport:
    @staticmethod
    def generate_report(score: int, status: str, viewports: dict) -> str:
        """
        Formats report summaries detailing viewports rendering paths.
        """
        report_md = f"""# Visual Preview Quality Audit Report
## Final Score: {score}/100
## Audit Status: {status}

---

### Viewport Screenshots Capture Index
"""
        for device, path in viewports.items():
            report_md += f"* **{device.capitalize()} Viewport Capture**: `{path}`\n"
            
        return report_md
