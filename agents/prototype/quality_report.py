from typing import Dict, List

class QualityReport:
    @staticmethod
    def generate_report(overall_score: int, cert_level: str, metrics: Dict[str, int]) -> str:
        """
        Formats report summaries.
        """
        return f"""# Quality Audit Certification Report
## Overall Score: {overall_score}/100
## Certification Level: {cert_level}

---

### Audit Dimension Scores Matrix
* **HTML Structure Tag Closures**: `{metrics.get('html')}`
* **Accessibility Landmark Indicators**: `{metrics.get('accessibility')}`
* **Performance Size Audits**: `{metrics.get('performance')}`
* **SEO Metadata Titles**: `{metrics.get('seo')}`
* **UX Layout Menus**: `{metrics.get('ux')}`
"""
