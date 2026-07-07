# Phase Exit Checklist: PEC-014
## Phase 7.7 - Template Intelligence Engine Checklist

This checklist defines the mandatory gates that Phase 7.7 (Template/Layout Intelligence Engine) must pass before it can be marked as **LOCKED**.

---

### Phase Definition
* **Target Phase**: Phase 7.7 — Template Intelligence Engine
* **Verification Date**: 2026-07-05
* **Lead Engineer**: Antigravity
* **QA Auditor**: Independent Enterprise QA Auditor

---

## 1. Architecture Gate
- [ ] **Structural Compliance**: Code contains separate helper modules as specified in EDK: `layout_selector.py`, `grid_builder.py`, `sequence_sorter.py`, `spacing_rules.py`, `layout_validator.py`, and `layout_models.py`.
- [ ] **Strict Isolated Compilation**: Layer functions purely as a structural grid assembler without external script injections.
- [ ] **Database Schema**: `prototype_templates` table has been migrated successfully in SQLite database with job foreign keys.

---

## 2. Validation & Safety Gates
- [ ] **Missing Block Rendering Protection Rules**:
  * Missing layout wrappers (such as header or footer) are auto-injected by the grid builder to secure page integrity.
- [ ] **Invalid Element Filter Controls**:
  * Sections featuring invalid characters or malformed sizes are sanitised and mapped to default fallback grid sizes.
- [ ] **Deduplication Check**: Re-running the layout engine updates existing database template rows instead of duplicate insertions.

---

## 3. Testing Gate
- [ ] **Unit Testing**: Tests verify:
  * Tailwind column spanning class conversions.
  * Section layout sequencing order sorting rules.
  * Missing section auto-injections.
- [ ] **Integration Testing**: Pipeline checks that output matches template schema and inserts state inside database.

---

## 4. Documentation Gate
- [ ] **Master Plan Synced**: Status updated correctly in MASTER_PLAN.md.
- [ ] **Sign-off Complete**: Audited walkthrough and test reports complete.
