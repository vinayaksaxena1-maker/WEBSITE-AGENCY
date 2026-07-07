# Software Design Document: SDD-017
## Phase 7.10 - Preview Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Preview Engine ka main role compiled HTML prototype files ko load karke presentation-ready visual preview screenshots capture karna, side-by-side Before/After rendering comparisons build karna, aur local previews quality score metrics compute karna hai. This component functions purely as a local renderer validator without external API token consumption.

---

## 2. Temporary Local Routing Mechanics
* **Local Web Server**:
  * Engine mounts a lightweight local server (e.g. using Python's `http.server` or custom asyncio servers) on a configurable local port (default: `8000`).
  * Hosts the build directory (`output/prototypes/`) so Playwright or visual capture tools can load `index.html` and resolve relative paths (`assets/css/index.css`, `assets/images/`) locally.

---

## 3. Side-by-Side Before/After Alignment Schema
Generates visual comparison mappings of layouts:

| Side | Source Asset | Captured Viewport | Description |
| :--- | :--- | :--- | :--- |
| **Before** | Original target crawler screenshot | 1280px Width | Legacy screenshot representation of the target site |
| **After** | Upgraded generated index.html preview | 1280px Width | Upgraded responsive blueprint rendering |

The comparison module combines both images into a side-by-side or overlay representation saved inside the output comparison folder directory (`output/comparison/`).

---

## 4. Database Schema: `prototype_previews`
SQLite dialect conformed schema representation:

### Table: `prototype_previews`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `preview_version` | `String(50)` | Nullable=False, Default='1.0.0' | SemVer preview layout version |
| `desktop_image` | `String(300)` | Nullable=True | relative path to desktop viewport screenshot |
| `laptop_image` | `String(300)` | Nullable=True | relative path to laptop viewport screenshot |
| `tablet_image` | `String(300)` | Nullable=True | relative path to tablet viewport screenshot |
| `mobile_image` | `String(300)` | Nullable=True | relative path to mobile viewport screenshot |
| `comparison_image` | `String(300)` | Nullable=True | relative path to side-by-side comparison image |
| `preview_score` | `Integer` | Nullable=False | Calculated preview validation score (0-100) |
| `status` | `String(50)` | Nullable=False, Default='COMPLETED' | Preview compilation state |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
