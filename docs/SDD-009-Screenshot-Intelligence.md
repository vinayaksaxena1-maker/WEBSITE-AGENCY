# Software Design Document: SDD-009
## Phase 7.2 - Screenshot Intelligence Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Screenshot Intelligence Engine ka main objective business websites ke accurate, high-quality, and standardized visual screenshots capture karna hai. Yeh captures downstream prototype design analysis, theme matching, and visual auditing ke liye use honge. Engine fully deterministic hai (zero AI inference).

---

## 2. Headless Playwright Configuration
Playwright headless mode configuration details:
* **Headless**: True (default).
* **Browsers**: Chromium (preferred), WebKit, Firefox (fallback).
* **Launch Timeout**: Strict `< 5 seconds`.
* **Viewport Dimensions**:
  * Desktop: `1920 × 1080` (Preferred)
  * Laptop: `1440 × 900`
  * Tablet: `768 × 1024`
  * Mobile: `390 × 844`
* **Additional flags**:
  * `--disable-notifications` (Enabled)
  * `--disable-extensions` (Enabled)
  * `--disable-gpu` (Enabled, for headless environments stability)
  * **User Agent**: Configurable desktop and mobile strings.
  * **Timezone & Locale**: Enforced UTC and sRGB colorspace representation.

---

## 3. Scroll Strategy & Lazy Loading Bypass
Lazy-loaded images, dynamic components, and cards ko force rendering ke liye Scroll Engine niche likhe strategy execute karega:
1. **Initial Page Navigation**: DOMContentLoaded aur Network Idle states wait karna.
2. **Incremental scrolling**: Page scroll view ko bottom tak incremental jumps (e.g., 250px increments with 50-100ms pause) ke sath scroll karna.
3. **Viewport Stability Check**: Ensure animations pause/freeze aur active loading indicators stable ho chuke hain.
4. **Return to Top**: Page position ko smooth scroll se coordinate `(0, 0)` par wapas reset karna before capturing.
5. **Full Page Capture**: Complete viewport snapshot fetch karna.

---

## 4. Cookie & Popup Handling Rules
Visual clutter clear karne ke liye dynamic overlays dismiss karna:
* **Popup categories to handle**:
  * Cookie Consent Banners
  * Newsletter Overlays
  * Location & Notification prompts
  * Chat Widgets (e.g. Intercom, HubSpot)
* **Strategy**:
  * Common CSS selectors and XPath queries ka matching database (e.g., `#cookie-accept`, `.consent-close`, `#newsletter-dismiss`, `[aria-label="dismiss"]`) close trigger karne ke liye target karna.
  * Graceful fallback if selector fails: Log detailed warning, suppress errors, and continue screenshot capture.

---

## 5. Database Schema: `prototype_screenshots`
Dialect-safe representation in SQLite:

### Table: `prototype_screenshots`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `desktop_path` | `String(255)` | Nullable=False | Relative filesystem path to desktop screenshot PNG |
| `tablet_path` | `String(255)` | Nullable=False | Relative filesystem path to tablet screenshot PNG |
| `mobile_path` | `String(255)` | Nullable=False | Relative filesystem path to mobile screenshot PNG |
| `fullpage_path` | `String(255)` | Nullable=False | Relative filesystem path to full-page screenshot PNG |
| `capture_duration` | `Float` | Nullable=False | Execution elapsed time in seconds |
| `page_height` | `Integer` | Nullable=False | Measured vertical length of resolved DOM in pixels |
| `page_width` | `Integer` | Nullable=False | Measured width of resolved DOM in pixels |
| `browser` | `String(50)` | Nullable=False | Browser platform (e.g. chromium, Webkit) |
| `status` | `String(50)` | Nullable=False, Default='CAPTURED' | Visual extraction state |
| `created_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware timestamp (UTC) |
