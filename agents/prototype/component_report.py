from typing import List, Dict, Any

class ComponentReport:
    @staticmethod
    def generate_report(components: List[Dict[str, Any]], tree: Dict[str, Any], validation_summary: Dict[str, Any]) -> str:
        """
        Generates markdown audit reports listing compiled UI components structures.
        """
        comp_rows = []
        for c in components:
            comp_rows.append(
                f"| `{c['instance_id']}` | `{c['name']}` | `{c['variant']}` | `{c['priority']}` | `{', '.join(c.get('dependencies', [])) or 'None'}` |"
            )

        report_md = f"""# Component Layout Compilation Report
## Total Compiled: {len(components)}

---

### 1. Reusable Components Registry Table
| Instance ID | Component Name | Style Variant | Priority | Dependencies |
| :--- | :--- | :--- | :--- | :--- |
{"\n".join(comp_rows)}

---

### 2. Nesting Tree Summary Hierarchy
* **Root**: `{tree['instance_id']}` (Depth: 0)
"""
        for child in tree.get("children", []):
            report_md += f"  * Child: `{child['instance_id']}` (Depth: {child['depth']}, Priority: {child.get('priority', 'Medium')})\n"
            for gchild in child.get("children", []):
                report_md += f"    * Grandchild: `{gchild['instance_id']}` (Depth: {gchild['depth']})\n"

        report_md += f"""
---

### 3. Compliance & Validations Checklist
* **Layout Responsive Fluidity**: {"READY" if validation_summary.get("responsive_ready") else "FAILED"}
* **Accessibility Compliance (WCAG Markers)**: {"READY" if validation_summary.get("accessibility_ready") else "FAILED"}
* **Sanity Validation Status**: {"PASS" if validation_summary["success"] else "FAIL"}
"""
        return report_md
