# Phase Exit Checklist Template
## Enterprise Development Kit (EDK) Gatekeeper Policy

This document defines the mandatory exit gates that every phase of the Website Upgrade Agency development lifecycle must pass before it can be marked as **LOCKED** and transitioning to the next phase.

---

### Phase Definition
* **Target Phase**: [Phase Number & Name]
* **Verification Date**: [YYYY-MM-DD]
* **Lead Engineer**: [Name]
* **QA Auditor**: [Name]

---

## 1. Architecture Gate
This gate ensures that the code design complies with the high-level architecture constitution (SAS-001) and follows correct encapsulation and design patterns.

- [ ] **Structural Compliance**: Code is decoupled into clear components (models, services, filters, coordinators).
- [ ] **Dependency Rule**: Downstream layers do not import upstream orchestrators. Circular dependencies are zero.
- [ ] **Interface Contracts**: Dynamic subclasses conform to abstract base definitions or interfaces.
- [ ] **Database Standards**: Models map directly using SQLAlchemy ORM. All migrations or table creation scripts are documented.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 2. Testing Gate
This gate ensures the stability and code coverage of the implemented phase features.

- [ ] **Test Coverage Baseline**: Unit tests run and verify all critical code paths. Code coverage target $\ge 80\%$ (or explicit coverage metrics provided).
- [ ] **Error Path Testing**: Tests cover validation failures, network blocks, and mock fallbacks.
- [ ] **Async Verification**: All asynchronous methods are verified using standard `pytest-asyncio` fixtures.
- [ ] **Test Suite Run**: `python -m pytest -v` runs with zero warnings and zero failures.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 3. Security Gate
This gate enforces data protection and secure coding practices.

- [ ] **Secrets Management**: No API keys, passwords, database credentials, or tokens are hardcoded. Everything is loaded via Pydantic Settings from `.env`.
- [ ] **Input Sanitization**: All user inputs, scrapers, and external APIs are sanitized (e.g. domain normalization, regex escaping).
- [ ] **SQL Injection Prevention**: Database queries use parameterized SQLAlchemy constructs (`select()`, `insert()`). No raw string concatenations for database execution.
- [ ] **Resource Limits**: Regular expressions used for validation are bounded to prevent ReDoS vectors.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 4. Performance Gate
This gate ensures the application meets latency, CPU, and memory limits.

- [ ] **Latency Benchmark**: Core loop operations execute within target SLAs (e.g., search processing, scraping fallback latency).
- [ ] **Resource Usage**: Memory allocations and CPU peaks are within bounded limits.
- [ ] **Connection Lifecycle**: Connection pooling for Databases and Redis handles connection opening/closing safely without leaks.
- [ ] **Deduplication**: Duplicate lookups are indexed to avoid database query bottlenecks.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 5. Documentation Gate
This gate ensures codebase and architectural changes are transparently documented.

- [ ] **Software Design Document (SDD)**: SDD is written for the phase containing detailed data flow, schemas, and requirements mapping.
- [ ] **Inline Documentation**: Code uses clear docstrings explaining arguments, returns, and rationale for complex operations.
- [ ] **Master Plan Updated**: Current progress percentage and status of the current/next phases are updated in `docs/MASTER_PLAN.md`.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 6. QA Gate
This gate ensures that testing checks out under live simulated or production environments.

- [ ] **Functional Baseline**: The phase meets all specific EDK requirements (e.g. for Phase 1: Minimum 50 valid unique domains).
- [ ] **Live run validation**: Execution harness has been run on live or mock networks to verify database inserts and Redis queue payloads.
- [ ] **Exception Swallowing Check**: No mocked context managers or try-except blocks silently suppress critical logic exceptions.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 7. Audit Gate
This gate verifies that the audit documentation matches real measurements.

- [ ] **Evidence Tables**: The Independent QA Audit Report contains explicit verification tables for Databases, Redis, Tests, and Performance.
- **Audit Scores**: All sub-categories (Architecture, Infrastructure, Configuration, Logging, Database, Redis, Testing, Documentation) are scored individually.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

## 8. Lock Gate
The final sign-off confirming code freeze.

- [ ] **Walkthrough Complete**: A complete walkthrough is recorded, outlining all features built and verified.
- [ ] **Code Freeze**: All files belonging to this phase are declared immutable and marked as **LOCKED**.
- [ ] **Next Phase Authorization**: The Product Owner / Director officially signs off on entering the next phase.

*Gate Status*: **[PENDING / PASS / FAIL]**
*Objective Evidence / Comments*:
> 

---

### Sign-off
* **Lead Developer Sign-off**: ________________________ Date: ____________
* **QA Auditor Sign-off**: ________________________ Date: ____________
* **Product Owner Approval**: ________________________ Date: ____________
