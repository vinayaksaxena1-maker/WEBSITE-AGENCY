from typing import Dict, Any

class ResponsiveReport:
    @staticmethod
    def generate_report(blueprint: Dict[str, Any], score: int, status: str, elapsed: float) -> str:
        """
        Formats markdown report listing responsive breakpoint adaptations.
        """
        report_md = f"""# Responsive Intelligence Adaptation Report
## Elapsed Processing Time: {elapsed:.3f} seconds
## Quality Verification Score: {score}/100
## Audit Status: {status}

---

### 1. Viewport Adaptation Mapping Matrix
"""
        for device, rules in blueprint.items():
            report_md += f"""
#### Device Profile: `{device}`
* **Container Padding Constraint**: `{rules.get('padding_rule')}`
* **Grid Card Layout Style**: `{rules.get('card_layout')}`
* **Navigation Drawer Conversion Style**: `{rules.get('navigation_style')}`
"""
        return report_md
