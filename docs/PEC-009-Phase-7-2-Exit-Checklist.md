# Phase Exit Checklist: PEC-009
## Phase 7.2 - Screenshot Intelligence Engine Checklist

This checklist defines the mandatory gates that Phase 7.2 (Screenshot Intelligence Engine) must pass before it can be marked as **LOCKED**.

---

### Phase Definition
* **Target Phase**: Phase 7.2 — Screenshot Intelligence Engine
* **Verification Date**: 2026-07-05
* **Lead Engineer**: Antigravity
* **QA Auditor**: Independent Enterprise QA Auditor

---

## 1. Architecture Gate
- [ ] **Structural Compliance**: Engine contains separate helper modules as specified in EDK: `viewport_profiles.py`, `scroll_engine.py`, `lazy_loader.py`, `popup_handler.py`, `capture_engine.py`, and `image_optimizer.py`.
- [ ] **Zero AI Dependency**: Verification code contains zero generative model calls. Full rendering is handled via local browser instrumentation.
- [ ] **Database Schema**: `prototype_screenshots` table has been successfully migrated in SQLite with job_id foreign key constraint.

---

## 2. Performance Gate
- [ ] **Browser Startup Time**: Headless Playwright context initialization completed in `< 5 seconds`.
- [ ] **Image Compression Boundaries**:
  * Output screenshots use **lossless PNG** format.
  * Image optimization limits target maximum size `< 1.5MB` for fullpage capture and `< 500KB` for individual viewports.
  * Color profiling validates output images conform strictly to sRGB standard.
- [ ] **Deduplication Check**: Re-running the agent for same job updates paths instead of inserting duplicate rows.

---

## 3. Testing Gate
- [ ] **Unit Testing**: Tests verify:
  * Browser launch configurations and options.
  * Navigation timeout handling (graceful timeout limit).
  * Scrolling logic triggering and returning to coordinate (0, 0).
  * Auto-dismissal of cookie banners and popups.
- [ ] **Integration Testing**: Pipeline checks SQLite schema transactions and saves actual mockup screenshots on local mock file systems.

---

## 4. Security & Compliance Gate
- [ ] **No Permanent Cookies**: Cookie context is cleared after every browser session closure.
- [ ] **Robots.txt & Auth constraints**: Crawling respects standard scraping flags. No bypass of authentication gates.
- [ ] **Private Data Isolation**: Plaintext screenshots do not expose credentials or internal configuration keys.

---

## 5. Documentation Gate
- [ ] **Master Plan Synced**: Status updated correctly in MASTER_PLAN.md.
- [ ] **Sign-off Complete**: Verified audits and walkthrough logs created.
