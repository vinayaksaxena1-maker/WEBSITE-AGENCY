# Software Design Document: SDD-017
## Phase 7.8 - Responsive Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Responsive Intelligence Engine ka primary task approved layout blueprints, component structures, aur design presets themes ko combine karke multi-device compatible responsive blueprint specification compile karna hai. Yeh subsystem local specs transformer ki tarah function karega, bina generic AI APIs call kiye.

---

## 2. Breakpoint Profile System
The engine maps target screen width sizes to standard Tailwind breakpoint equivalents.

| Profile Name | Width Boundary Range | Target Devices | Grid Column Scaling |
| :--- | :--- | :--- | :--- |
| `Desktop XL` | `>= 1440px` | Large monitors | 12 Columns / Full Width |
| `Desktop` | `1280px - 1439px` | Standard Desktop | 12 Columns / Max Width 1280px |
| `Laptop` | `1024px - 1279px` | Laptops / iPads Landscape | 12 Columns / Max Width 1024px |
| `Tablet` | `768px - 1023px` | Tablets Portrait / iPad | 6 Columns / Max Width 768px |
| `Mobile Large` | `480px - 767px` | Landscape Phones | 4 Columns / Max Width 480px |
| `Mobile` | `360px - 479px` | Standard Mobile Portrait | 2 Columns / Full Width Fluid |
| `Small Mobile` | `< 360px` | Old/Small Mobile Phones | 1 Column / Full Width Fluid |

---

## 3. Container width & Layout Adaptation Rules
* **Max Width Rules**: Large screen sizes use static max-widths (`max-w-7xl`, `max-w-5xl`) with centering (`mx-auto`).
* **Fluid Width Rules**: Mobile and small mobile sizes switch to full width fluid structures (`w-full`) with horizontal padding offsets.

---

## 4. Typography & Spacing Scaling
* **Fluid Typography Scale**:
  * Heading fonts scale down on mobile screens to avoid overlap:
    * `h1`: 0.7x (Desktop 4xl -> Mobile 2xl)
    * `h2`: 0.8x (Desktop 3xl -> Mobile xl)
    * `h3`: 0.9x (Desktop 2xl -> Mobile lg)
    * `body`: 1.0x (remains readable, 1rem)
* **Fluid Spacing Scale**:
  * Section margins/paddings scale down on smaller viewports:
    * Desktop section padding: `py-16` / `py-20`
    * Mobile section padding: `py-8` / `py-10` (0.5x scaling)

---

## 5. Database Schema: `prototype_responsive`
SQLite dialect conformed schema representation:

### Table: `prototype_responsive`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `breakpoint_profile` | `Text` | Nullable=False | JSON string detailing breakpoints setup |
| `device_support` | `Text` | Nullable=False | JSON string listing supported viewports |
| `responsive_score` | `Integer` | Nullable=False | Calculated responsive quality score (0-100) |
| `validation_status` | `String(50)` | Nullable=False, Default='PASSED' | Verification audit status |
| `execution_time` | `Float` | Nullable=False | Processing execution time in seconds |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
