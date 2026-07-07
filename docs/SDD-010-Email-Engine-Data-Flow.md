# System Design Document (SDD-010)
## Phase 8.3, 8.4, and 8.5 - Data Contracts, Execution Workflow, & Context Assembly

This document specifies the Data Contracts (8.3), Execution Workflow orchestration (8.4), and Context Assembly Layer (8.5) design for the AI Personalized Email Engine.

---

### 1. Data Contracts (Phase 8.3)
All interactions within the AI Personalized Email Engine are governed by strongly typed data schemas defined using Pydantic. These contracts ensure schema validity, field constraints, and DTO immutability during execution.

#### 1.1 Core Contracts
* **`UnifiedInputPackage`**: Groups the validated upstream inputs:
  - `lead_profile`: `domain` (str), `niche` (str).
  - `audit_report`: `audit_score` (int), `mobile_score` (int).
  - `prototype_report`: `prototype_url` (str).
  - `contact_info`: `name` (str), `email` (str).
* **`UnifiedBusinessContext`**: Aggregated DTO produced by the Context Builder containing normalized fields.
* **`PersonalizationContext`**: Filtered context containing hook parameters and company nomenclature.
* **`AIPromptPackage`**: Structured system instruction payload ready for AI execution.
* **`GeneratedEmailDraft`**: Subject line and body draft text.
* **`ValidatedEmailDraft`**: Screened subject and body.
* **`FormattedEmailPackage`**: Structured HTML wrapped email.
* **`FinalEmailPackage`**: Combines the formatted HTML output with tracing metadata.

---

### 2. Execution Workflow (Phase 8.3 & 8.4)
The workflow coordinates sequential processing. If any module fails or a contract validation error occurs, execution halts immediately (fail-fast propagation).
```
Input manager DTO validation
      │
      ▼
Context assembly contract validation
      │
      ▼
Personalization variables check
      │
      ▼
AI prompt package validation
      │
      ▼
LLM execution response validation
      │
      ▼
Draft validator screen
      │
      ▼
HTML formatter validation
      │
      ▼
Metadata generation check
```

---

### 3. Context Assembly Layer (Phase 8.5)
The Context Assembly Layer gathers raw inputs, deduplicates values, and normalizes attributes:
* **Domain Normalization**: Converts all domains to lower-case, strips protocol headings (`http://`, `https://`, `www.`), and removes leading/trailing whitespaces.
* **Email Normalization**: Strips spaces and converts email addresses to lower-case.
* **Score Normalization**: Ensures scores lie within the bound `[0, 100]`.
* **String Normalization**: Cleans whitespaces from company names and contact names.
