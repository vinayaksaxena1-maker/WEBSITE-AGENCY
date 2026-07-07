# System Design Document (SDD-013)
## Phase 8.9, 8.10, and 8.11 - Email Validation, Output Formatting, & Metadata Generation Layers

This document outlines the design specifications, validation checks, formatting rules, and metadata parameters for the remaining layers of the AI Personalized Email Engine.

---

### 1. Email Validation Layer (Phase 8.9)
The Validation Layer is responsible for verifying structural, personalization, factual, and communication compliance before publication:
* **Structural Checkpoints**:
  - `Subject presence`: Subject line string cannot be empty.
  - `Greeting presence`: Body must begin with a greeting (e.g. "Hi", "Hello", "Dear").
  - `Call-To-Action (CTA) presence`: Body must contain a link or a mention of the prototype preview (e.g., matching a URL or the word "prototype").
  - `Professional closing`: Body must end with a standard closing (e.g., "Best regards", "Sincerely").
  - `Signature presence`: Signature block must be present (e.g. "Website Agency").
* **Quality & Tone Checkpoints**:
  - `Personalization coverage`: Rejects the draft if any unresolved placeholders like `{variable}` or `[Placeholder]` are present.
  - `Communication quality`: Professional business language check.
* **Validation Report Structure**:
```json
{
  "validation_id": "<uuid>",
  "status": "PASS | FAIL",
  "checked_at": "<iso_timestamp>",
  "categories": {
    "structural": "PASS | FAIL",
    "personalization": "PASS | FAIL",
    "communication": "PASS | FAIL",
    "factual": "PASS | FAIL",
    "formatting": "PASS | FAIL"
  },
  "errors": []
}
```

---

### 2. Output Formatting Layer (Phase 8.10)
Standardizes document formats without altering validated text content:
* **Line Normalization**:
  - Collapses consecutive blank lines (> 2) into standard single paragraphs.
  - Trims trailing and leading spaces from text bodies.
* **HTML Wrapping**:
  - Wraps formatted paragraph layouts into a responsive modern container template.

---

### 3. Metadata Generation Layer (Phase 8.11)
Seals the package with tracing metadata required by downstream engines (CRM, follow-ups):
* **Metadata Fields**:
  - `execution_id`: UUID4 string.
  - `generated_at`: ISO-8601 UTC timestamp.
  - `engine_version`: "EMAIL-1.0".
  - `validation_status`: overall PASS/FAIL.
