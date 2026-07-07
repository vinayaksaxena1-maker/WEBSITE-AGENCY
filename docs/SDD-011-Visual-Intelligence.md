# Software Design Document: SDD-011
## Phase 7.4 - Visual Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Visual Intelligence Engine ka main objective target website ke CSS styles, inline style elements, and computed stylesheet attributes to analyze karke deterministic primary, secondary, background, and text colors extract karna hai. Yeh component read-only layout metadata provider ki tarah function karega, without executing AI model inference.

---

## 2. Deterministic CSS Token Parsing & Color Normalization
* **CSS Parsing**:
  * Cleaned HTML block elements me standard CSS attributes (e.g. `color`, `background-color`, `font-family`) ke key-value style pairs map karna.
  * Inline styles attribute values parse karna using regex patterns.
* **HEX/RGBA Color Model Normalization Matrix**:
  * Input configurations like `rgb(r, g, b)`, `rgba(r, g, b, a)`, `#rgb`, `#rrggbb`, or text color names (e.g. `red`, `blue`) ko normalize karke uppercase hex string format (e.g. `#FFFFFF`, `#1A365D`) me convert karna.
  * Invalid color representation handles strictly fallback color mapping.

| Input Format | Normalized Format | Fallback (If Invalid) |
| :--- | :--- | :--- |
| `rgb(30, 58, 138)` | `#1E3A8A` | `#FFFFFF` |
| `rgba(30, 58, 138, 0.5)` | `#1E3A8A` (Drop Alpha) | `#FFFFFF` |
| `#1e3` | `#11EE33` | `#FFFFFF` |
| `invalid-color` | `#FFFFFF` | `#FFFFFF` |

---

## 3. Primary/Secondary Style Extraction Workflows
1. **Body Scan**: Body tag ke primary computed style attributes detect karke dominant background aur text color identify karna.
2. **Interactive Node Scans**: Primary/secondary action links, headers, nav tags, buttons detect karke unke styles aggregate aur count mapping generate karna.
3. **Weight Sorting**: Extracted colors list ko frequency mapping ke basis par sort karna:
   * **Primary Color**: Most frequent color found on buttons and semantic header/footer wrappers.
   * **Secondary Color**: Second most frequent theme color.
   * **Background Color**: Dominant body background.
   * **Text Color**: Dominant body text color.

---

## 4. Database Schema: `prototype_visual_analysis`
SQLite dialect conformed schema:

### Table: `prototype_visual_analysis`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `primary_color` | `String(7)` | Nullable=False | Normalized primary theme color hex |
| `secondary_color` | `String(7)` | Nullable=False | Normalized secondary theme color hex |
| `background_color` | `String(7)` | Nullable=False | Normalized background color hex |
| `text_color` | `String(7)` | Nullable=False | Normalized text color hex |
| `font_family` | `String(100)` | Nullable=False | Primary font family string |
| `visual_score` | `Integer` | Nullable=False | Computed layout complexity score (0-100) |
| `analysis_time` | `Float` | Nullable=False | Elapsed parsing duration in seconds |
| `status` | `String(50)` | Nullable=False, Default='ANALYZED' | Structural validation state |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
