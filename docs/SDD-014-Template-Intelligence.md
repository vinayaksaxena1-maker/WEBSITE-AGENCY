# Software Design Document: SDD-014
## Phase 7.7 - Template Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Template Intelligence Engine (traditionally called Layout Intelligence Engine) ka primary role website grids layouts structures, layout columns, section sequencing order, and spacings templates compile karna hai downstream code assembly modules ke liye. Yeh sub-engine no external code injections features key-points support karta hai.

---

## 2. Tailwind CSS Column Translation Matrix
The engine translates abstract grid structures to Tailwind CSS column spanning class markers.

| Column Layout Target | Tailwind Desktop Class | Tailwind Tablet Class | Tailwind Mobile Class |
| :--- | :--- | :--- | :--- |
| `1 Column` (Full Width) | `col-span-12` | `col-span-12` | `col-span-12` |
| `2 Columns` (Split Half) | `lg:col-span-6` | `md:col-span-6` | `col-span-12` |
| `3 Columns` (Thirds) | `lg:col-span-4` | `md:col-span-6` | `col-span-12` |
| `4 Columns` (Quarters) | `lg:col-span-3` | `md:col-span-6` | `col-span-12` |
| `Bento Grid Layout` | Dynamic mix (e.g. `col-span-8` & `col-span-4`) | `md:col-span-6` | `col-span-12` |

---

## 3. Section Layout Sequencing Rules
Standard sequencing rules verify user-flow logic. Any unmapped or random items are sorted to conform with standard website arrangements.

1. **Header / Navigation**: First element (always).
2. **Hero Section**: Primary branding banner (always second).
3. **Services / Features / Products**: Core offerings blocks.
4. **Trust / Testimonials / Reviews**: Social proof elements.
5. **FAQ / Accordion**: Secondary details sections.
6. **Contact Form / Form Panels**: Conversion actions triggers.
7. **Footer / Copyrights**: Last element (always).

---

## 4. Database Schema: `prototype_templates`
SQLite dialect conformed schema representation:

### Table: `prototype_templates`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `layout_type` | `String(50)` | Nullable=False | Type of layout grid (e.g. `one-page-app`) |
| `columns_count` | `Integer` | Nullable=False | Number of grid columns |
| `section_sequence` | `Text` | Nullable=False | Comma-separated section names sequence |
| `tailwind_grid_class` | `String(100)` | Nullable=False | Tailwind class string (e.g. `grid grid-cols-12`) |
| `spacing_rules` | `Text` | Nullable=False | Spacing values JSON string |
| `status` | `String(50)` | Nullable=False, Default='STRUCTURED' | Layout validation status |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
