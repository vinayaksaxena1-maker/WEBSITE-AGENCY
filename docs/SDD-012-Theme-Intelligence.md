# Software Design Document: SDD-012
## Phase 7.5 - Theme Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Theme Intelligence Engine ka goal business lead/industry segment aur computed visual style inputs ke basis par optimal design theme select karna hai. Yeh component rule-based token mappings generate karega jo downstream layout grid components assembly and CSS generation frameworks use karenge. No external generative AI engine calls.

---

## 2. Niche-to-Design Token Mapping Matrices
Industries are mapped to standard presets containing colors, typography, spacing, border system, and animations.

| Niche / Industry | Design Category | Personality | Primary Color | Secondary Color | Accent Color | Heading Font | Body Font |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `hospital` / `clinic` | Medical | Clean / High Trust | `#0F766E` (Teal) | `#0D9488` | `#F59E0B` | `Inter` | `Inter` |
| `fitness` | Bold Marketing | Energetic Dark | `#EA580C` (Orange) | `#1E1B4B` | `#F59E0B` | `Oswald` | `Roboto` |
| `restaurant` | Friendly | Warm / Cozy | `#DC2626` (Red) | `#F59E0B` | `#10B981` | `Playfair Display` | `Lato` |
| `law firm` | Corporate | Traditional | `#1E3A8A` (Navy) | `#475569` | `#D97706` | `Merriweather` | `Open Sans` |
| `technology` / `software` | Technology | Innovative / Modern | `#4F46E5` (Indigo) | `#7C3AED` | `#10B981` | `Outfit` | `Inter` |
| `fashion` | Premium Luxury | Minimal / Elegant | `#111827` (Charcoal) | `#6B7280` | `#D97706` | `Playfair Display` | `Montserrat` |
| *default* | Modern Business | Reliable | `#1E3A8A` (Navy) | `#3B82F6` | `#F59E0B` | `Inter` | `sans-serif` |

---

## 3. Token Generation Systems
* **Colors System**:
  * Normalizing background color (`#FFFFFF` default for light, `#0F172A` for dark theme presets).
  * Surface and Text colors generation following proper visual weights guidelines.
* **Typography System**:
  * CSS font scales mapping standard headings from `h1` to `h6`.
* **Border System**:
  * Theme border radius parameters (e.g. `card_radius`: `8px`, `button_radius`: `9999px` for pill style in modern presets).
* **Elevation / Shadows System**:
  * CSS box shadows configurations (small, medium, large layers).

---

## 4. Database Schema: `prototype_themes`
SQLite dialect conformed representation:

### Table: `prototype_themes`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `theme_name` | `String(100)` | Nullable=False | Name of the matched theme preset |
| `industry` | `String(100)` | Nullable=False | Input business category niche |
| `personality` | `String(100)` | Nullable=False | Brand personality classification |
| `primary_color` | `String(7)` | Nullable=False | Normalized Hex primary color |
| `secondary_color` | `String(7)` | Nullable=False | Normalized Hex secondary color |
| `accent_color` | `String(7)` | Nullable=False | Normalized Hex accent color |
| `heading_font` | `String(100)` | Nullable=False | Heading font family |
| `body_font` | `String(100)` | Nullable=False | Body text font family |
| `theme_score` | `Integer` | Nullable=False | Rating score (0-100) computed by validation checks |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
