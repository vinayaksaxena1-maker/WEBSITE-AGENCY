# QA Test Plan: QAP-003
## Website Audit Engine Test Specification

### 1. Objectives & Scope
This QA Plan establishes the testing protocols, test cases, and quality gates for the Website Audit Engine (Phase 2). It guarantees that all HTML parsing rules, scoring metrics, and database transactions perform correctly across normal execution paths, edge cases, and fallback states.

---

### 2. Test Execution Environment & Setup
* **Testing Library**: PyTest with `pytest-asyncio` plugin.
* **Test Database**: SQLite memory database (`sqlite+aiosqlite:///:memory:`) to ensure fast, isolated executions.
* **Mocking Tools**: `unittest.mock` for network connection pings, HTTP socket calls, and Playwright page loads.

---

### 3. Test Cases Specification

#### Test Case 1: SSL Verification Logic
* **Objective**: Verify that valid/invalid SSL configurations are correctly diagnosed.
* **Execution**: Mock the socket connection wrapper to return certificates with valid expiration dates and, separately, expired certificates.
* **Expected Result**: Expiry triggers score reductions; CA issuer details are correctly logged.

#### Test Case 2: SEO Meta Tag Parsing
* **Objective**: Verify that title tags, meta descriptions, and heading setups are correctly identified.
* **Execution**: Load static mock HTML payloads:
  * Payload A: Full title, meta description, single H1, multiple H2s.
  * Payload B: Empty title, missing meta, multiple H1s.
* **Expected Result**: Payload A scores 100 on SEO; Payload B scores lower based on logic matrices in SDD-003.

#### Test Case 3: Mobile Viewport Checks
* **Objective**: Assert viewport presence checks.
* **Execution**: Inject HTML payloads missing `<meta name="viewport">` tag.
* **Expected Result**: Mobile responsiveness score is correctly penalized.

#### Test Case 4: Performance Load Timing Fallbacks
* **Objective**: Verify response timing calculations under mock conditions.
* **Execution**: Mock `aiohttp` get request return timing using `asyncio.sleep` delays.
* **Expected Result**: Page Load times reflect sleep duration, scoring category correctly based on intervals.

#### Test Case 5: Transactional Database Insertion & Foreign Keys
* **Objective**: Ensure audits are inserted atomically and bound to their parent leads.
* **Execution**: Run database transactions trying to insert audits for non-existent lead IDs, and check cascade deletes.
* **Expected Result**: Foreign key violation error raised for invalid IDs; deleting parent leads deletes child audits cleanly.

#### Test Case 6: Duplicate Audit Checks
* **Objective**: Prevent duplicate audits from clogging database tables.
* **Execution**: Write duplicate audit records for same `lead_id`.
* **Expected Result**: Database unique constraints enforce error rollback.

---

### 4. Code Coverage Metrics
* **Goal**: Maintain code coverage $\ge 90\%$ for `agents/audit/` directories.
* **Coverage Verification Command**:
  ```powershell
  coverage run -m pytest -v
  coverage report -m
  ```
