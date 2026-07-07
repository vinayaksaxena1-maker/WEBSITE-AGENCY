from typing import Dict, Any

class ThemeReport:
    @staticmethod
    def generate_report(
        theme: Dict[str, Any],
        validation: Dict[str, Any],
        tokens: Dict[str, Any],
        score: int
    ) -> str:
        """
        Generates a readable markdown recommendation audit report explaining
        the chosen design preset, typography weights, and accessibility ratios.
        """
        report_md = f"""# Design Theme Recommendation Audit Report
## Presets Selected: {theme['name']}

---

### 1. Brand Identity & Niche
* **Industry / Niche**: {theme.get('category', 'Modern Business')}
* **Visual Personality**: {theme.get('personality', 'Clean / Professional')}
* **Calculated Match Score**: {score}/100

---

### 2. Styling Colors Palette
* **Primary Branding Color**: `{theme['colors']['primary']}`
* **Secondary theme Color**: `{theme['colors']['secondary']}`
* **Accent Highlight Color**: `{theme['colors']['accent']}`
* **Canvas Background Color**: `{theme['colors']['background']}`
* **Body Text Color**: `{theme['colors']['text']}`

---

### 3. WCAG Accessibility Audit
* **Text Contrast Ratio**: {validation['text_bg_ratio']:.2f}:1
* **Primary Contrast Ratio**: {validation['primary_bg_ratio']:.2f}:1
* **WCAG AA Compliance (Standard Text)**: {"PASS" if validation['passes_wcag_standard'] else "FAIL"}
* **WCAG AA Compliance (Large Text)**: {"PASS" if validation['passes_wcag_large'] else "FAIL"}

---

### 4. Typography Scale System
* **Heading Font Family**: `{theme['typography']['heading']}`
* **Body Font Family**: `{theme['typography']['body']}`
* **Heading 1 Font Size**: `{tokens['typography']['font_size_h1']}`
* **Body Text Font Size**: `{tokens['typography']['font_size_body']}`
* **Default Border Radius**: `{tokens['radius']['button']}`
"""
        return report_md
