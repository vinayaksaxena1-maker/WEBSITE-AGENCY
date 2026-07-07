# Phase Exit Checklist: PEC-016
## Phase 7.9 - HTML Generation Engine Checklist

This checklist defines the mandatory gates that Phase 7.9 (HTML Generation Engine) must pass before it can be marked as **LOCKED**.

---

### Phase Definition
* **Target Phase**: Phase 7.9 — HTML Generation Engine
* **Verification Date**: 2026-07-05
* **Lead Engineer**: Antigravity
* **QA Auditor**: Independent Enterprise QA Auditor

---

## 1. Architecture Gate
- [ ] **Structural Compliance**: Code contains separate helper modules as specified in EDK: `tailwind_generator.py`, `component_renderer.py`, `token_injector.py`, `accessibility_generator.py`, `seo_generator.py`, `schema_generator.py`, `asset_manager.py`, `build_optimizer.py`, `html_validator.py`, and `build_report.py`.
- [ ] **Strict Isolated File Builder**: Engine operates strictly as a local templates compiler with zero external asset dependencies or API invocation rules.
- [ ] **Database Schema**: `prototype_builds` table has been migrated successfully in SQLite database with job foreign keys.

---

## 2. Validation & Security Gates
- [ ] **HTML Tag Closing Compliance**:
  * Output HTML must be checked by validation libraries (e.g. `html5lib` or BeautifulSoup validators) to verify all nodes are closed and correct.
- [ ] **Relative Path Asset Isolation**:
  * Image/icons assets relative paths must reside strictly within directory subfolders (`assets/images`, `assets/css`) with dynamic external injections blocked.
- [ ] **FinOps Indicators**:
  * Tracks output index.html file sizes (warn if file size > 500 KB to keep loading time low).
- [ ] **Deduplication Check**: Re-running the generation updates existing database template rows instead of duplicate insertions.

---

## 3. Testing Gate
- [ ] **Unit Testing**: Tests verify:
  * Complete HTML syntax parsing validations.
  * Tailwind CSS theme variable injection.
  * SEO metadata insertions.
  * Relative asset directory path security.
- [ ] **Integration Testing**: Pipeline checks that output matches generation templates schema and inserts state inside database.

---

## 4. Documentation Gate
- [ ] **Master Plan Synced**: Status updated correctly in MASTER_PLAN.md.
- [ ] **Sign-off Complete**: Audited walkthrough and test reports complete.
