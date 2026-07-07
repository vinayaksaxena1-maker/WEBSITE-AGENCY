# Software Design Document: SDD-013
## Phase 7.6 - Component Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Component Intelligence Engine ka main goal parsed DOM structure block elements, style metrics, and theme configs ko process karke reusable UI component metadata assemblies compile karna hai. Yeh engine HTML output render nahi karega; iska role purely semantic component mapping definitions construct karna hai downstream HTML generation engine ke consumption ke liye.

---

## 2. DOM-to-Component Conversion Algorithms & Block Extractions
* **DOM-to-Component Mapping**:
  * Input DOM sections list (e.g. `hero`, `services`, `faq`) ko standard enterprise UI components me map karna.
  * Tag counts, CTA buttons count, forms complexity check karke matching component presets locate karna.
* **Block Extraction Definitions**:

| Parsed Section Zone | Extracted Component | Selection Criteria | Default Variant |
| :--- | :--- | :--- | :--- |
| `hero` | `HeroComponent` | Matches primary CTA buttons & heading levels | `modern` / `corporate` |
| `testimonials` / `reviews` | `TestimonialsComponent` | Scans text density and card arrays | `card-carousel` |
| `faq` | `FAQComponent` | Analyzes list structures, tabs, or accordions | `accordion` |
| `contact` / `inquiry` | `ContactFormComponent` | Locates form inputs, textareas, and submit buttons | `split-two-columns` |
| `restaurant menu` | `MenuComponent` | Checked if industry matches `restaurant` | `grid-list` |
| `doctors` / `clinical` | `DoctorsComponent` | Checked if industry matches `medical` | `department-tabs` |

---

## 3. Component Dependencies & Hierarchy Assembly
* **Dependency Validation**:
  * Hero component requires at least one primary CTA.
  * Form component requires input elements and button elements.
  * Footer component requires copyright markers and nav links.
* **Component Tree Structure**:
  * Website wrapper node acting as root parent.
  * Parent-child hierarchies nested properly (e.g. `Header ➔ Navigation`, `Section ➔ Card Grid ➔ Card`).

---

## 4. Database Schema: `prototype_components`
SQLite dialect conformed schema representation:

### Table: `prototype_components`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Index | Parent prototype job ID reference |
| `component_name` | `String(100)` | Nullable=False | Name of the parsed UI component |
| `variant` | `String(50)` | Nullable=False | Theme variant selection |
| `theme` | `String(100)` | Nullable=False | Assigned design theme profile |
| `priority` | `String(20)` | Nullable=False | Component importance (Critical/High/Medium/Low) |
| `dependencies` | `Text` | Nullable=True | Comma-separated list of required component types |
| `responsive_ready` | `Boolean` | Nullable=False, Default=True | Layout fluid responsiveness status |
| `accessibility_ready` | `Boolean` | Nullable=False, Default=True | Accessibility markers present flag |
| `status` | `String(50)` | Nullable=False, Default='COMPILED' | Compilation stage identifier |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
