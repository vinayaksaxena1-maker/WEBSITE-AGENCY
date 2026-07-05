# Software Design Document: SDD-010
## Phase 7.3 - DOM Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
DOM Intelligence Engine ka primary task HTML page layouts ke raw source ko read karke use clean, preprocessed, aur logical semantic structural map me convert karna hai. Yeh map layout generator aur component engines ke liye core foundation input serve karega. Yeh sub-engine completely read-only, non-executable, and deterministic hai (no AI models, no JS execution).

---

## 2. DOM Preprocessing & Noise Elimination
Raw DOM se clutter aur noise filter karne ke rules:
* **Excluded Node Categories**:
  * Scripts (`<script>`) aur style declarations (`<style>`).
  * Tracking pixels, analytics snippets, ads wrappers, inline SVGs (unless semantic icons), comments (`<!-- ... -->`).
  * Hidden nodes (elements carrying `display: none`, `visibility: hidden` or `aria-hidden="true"`).
* **DOM Normalization**:
  * Nested empty wrappers aur redundant divs collapse karna.
  * Whitespaces trim karna aur self-closing tag formats normalize karna.

---

## 3. Semantic Tag Detection Routines
Logical content blocks recognize karne ke filters:
* **Core Layout Tags**:
  * `<header>` & `<footer>` (Primary branding and utility blocks).
  * `<nav>` (Main/secondary navigation menu identification).
  * `<main>`, `<section>`, `<article>`, `<aside>` (Content zones partitioning).
* **Interactive Elements**:
  * `<form>` (Lead capture and input zones).
  * `<button>` & `<a>` (Actions and CTAs).
* **Grouping loops**:
  * `<ul>`, `<ol>`, `<dl>` lists parsing to detect menu arrays and grids.

---

## 4. Output Component Map Contract
Normalized DOM tree structure JSON output format:

```json
{
  "page_url": "https://example.com",
  "navigation": {
    "type": "sticky-header",
    "links": ["Home", "About", "Services", "Contact"]
  },
  "sections": [
    {
      "id": "sec-0",
      "type": "hero",
      "title": "Welcome to our Clinic",
      "ctas": [{"text": "Book Now", "href": "#book"}]
    },
    {
      "id": "sec-1",
      "type": "features",
      "cards_count": 3
    }
  ],
  "forms": [
    {
      "id": "contact-form",
      "fields_count": 4
    }
  ]
}
```

---

## 5. Database Schema: `prototype_dom_analysis`
SQLite dialect conformed storage:

### Table: `prototype_dom_analysis`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `component_count` | `Integer` | Nullable=False | Total parsed UI components |
| `section_count` | `Integer` | Nullable=False | Count of identified page sections |
| `navigation_type` | `String(50)` | Nullable=False | Classified nav design pattern (e.g. Hamburger) |
| `layout_type` | `String(50)` | Nullable=False | Resolved layout structure (e.g. Bento grid) |
| `cta_count` | `Integer` | Nullable=False | Count of interactive CTA nodes |
| `form_count` | `Integer` | Nullable=False | Count of detected dynamic forms |
| `analysis_time` | `Float` | Nullable=False | Execution speed in seconds |
| `status` | `String(50)` | Nullable=False, Default='ANALYZED' | Structural validation state |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
