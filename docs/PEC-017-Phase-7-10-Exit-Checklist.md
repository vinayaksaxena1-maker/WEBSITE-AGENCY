# Phase Exit Checklist: PEC-017
## Phase 7.10 - Preview Engine Checklist

This checklist defines the mandatory gates that Phase 7.10 (Preview Engine) must pass before it can be marked as **LOCKED**.

---

### Phase Definition
* **Target Phase**: Phase 7.10 — Preview Engine
* **Verification Date**: 2026-07-05
* **Lead Engineer**: Antigravity
* **QA Auditor**: Independent Enterprise QA Auditor

---

## 1. Architecture Gate
- [ ] **Structural Compliance**: Code contains separate helper modules as specified in EDK: `preview_server.py`, `render_validator.py`, `device_renderer.py`, `comparison_engine.py`, `preview_capture.py`, `preview_metadata.py`, and `preview_report.py`.
- [ ] **Strict Isolated Server**: Server executes locally on temporary ports, ensuring cleanup of sockets and threads upon completion.
- [ ] **Database Schema**: `prototype_previews` table has been migrated successfully in SQLite database with job foreign keys.

---

## 2. Validation & Security Gates
- [ ] **Session Asset Cleanup**:
  * Temporary files and server sockets are cleaned up post-compilation, leaving zero zombie processes.
- [ ] **Viewport Layout Overflow Checks**:
  * Asserts rendering correctness checking for visual layout overflows, broken images links, or unexpected horizontal scrollbars.
- [ ] **FinOps Indicators**:
  * Warns if compilation duration exceeds 5 seconds.
- [ ] **Deduplication Check**: Re-running the preview engine updates existing database template rows instead of duplicate insertions.

---

## 3. Testing Gate
- [ ] **Unit Testing**: Tests verify:
  * Local preview server socket lifecycle and clean shutdown.
  * Multi-viewport snapshot scaling.
  * Visual comparison composite generation.
- [ ] **Integration Testing**: Pipeline checks that output matches preview schemas and inserts state inside database.

---

## 4. Documentation Gate
- [ ] **Master Plan Synced**: Status updated correctly in MASTER_PLAN.md.
- [ ] **Sign-off Complete**: Audited walkthrough and test reports complete.
