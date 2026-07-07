# Software Design Document: SDD-016
## Phase 7.9 - HTML Generation Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
HTML Generation Engine ka primary goal compiled responsive blueprints, selected theme design tokens, and components structures ko combine karke production-quality static semantic HTML5 prototypes and Tailwind CSS sheets write karna hai. Yeh sub-engine strictly as a local file writer/compiler function karega, without executing external API calls.

---

## 2. Semantic HTML5 Layout Synthesis Architecture
The engine compiles a flat or hierarchical list of responsive component specifications into static HTML5 semantic layout structures.

### Standard Semantic Tags Mapping
* `HeaderComponent` -> `<header role="banner">`
* `HeroComponent` / `MainContent` -> `<main role="main">`
* `SectionComponent` -> `<section>`
* `NavigationComponent` -> `<nav role="navigation">`
* `FooterComponent` -> `<footer role="contentinfo">`

---

## 3. Design Tokens Injection Loop
Branding typography and color choices are dynamically compiled into root CSS variables and injected into style wrappers.

```css
:root {
    --primary: [[primary_color]];
    --secondary: [[secondary_color]];
    --accent: [[accent_color]];
    --bg-surface: [[background_color]];
    --text-main: [[text_color]];
    --font-heading: [[heading_font]];
    --font-body: [[body_font]];
}
```

These parameters are substituted during prototype assembly and injected inside the HTML page `<head>` block.

---

## 4. Database Schema: `prototype_builds`
SQLite dialect conformed schema representation:

### Table: `prototype_builds`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `build_version` | `String(50)` | Nullable=False, Default='1.0.0' | SemVer build indicator version |
| `component_count` | `Integer` | Nullable=False | Total components rendered inside prototype |
| `html_size` | `Integer` | Nullable=False | Output HTML file size in bytes |
| `asset_count` | `Integer` | Nullable=False | Total associated stylesheet/script files assets |
| `seo_score` | `Integer` | Nullable=False | Calculated SEO validation score (0-100) |
| `accessibility_score` | `Integer` | Nullable=False | Calculated accessibility validation score (0-100) |
| `validation_status` | `String(50)` | Nullable=False, Default='PASSED' | HTML syntax validation status |
| `generation_time` | `Float` | Nullable=False | Elapsed processing compile duration |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
