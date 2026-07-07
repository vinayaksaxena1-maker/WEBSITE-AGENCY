# System Design Document (SDD-009)
## Phase 8.2 - AI Personalized Email Engine Internal Modules

This document outlines the purpose, inputs, outputs, and responsibilities for all 8 internal modules that form the AI Personalized Email Engine.

---

### 1. Module Overview & Dependency Diagram
```
Input Manager
      │  (Unified Input Package)
      ▼
Context Builder
      │  (Unified Business Context)
      ▼
Personalization Manager
      │  (Personalization Context)
      ▼
Prompt Builder
      │  (AI Prompt Package)
      ▼
AI Generation Manager
      │  (Generated Email Draft)
      ▼
Email Validator
      │  (Validated Email & Validation Report)
      ▼
Output Formatter
      │  (Formatted Email Package)
      ▼
Metadata Generator
      │  (Metadata & Final Email Package)
      ▼
Final Email Package
```

---

### 2. Module Specifications

#### 2.1 Input Manager
* **Purpose**: Load validated upstream data tables and configurations.
* **Responsibilities**:
  - Fetch target lead profile and contact records.
  - Load speed and visual audit findings.
  - Query theme selection and prototype references.
  - Validate that mandatory parameters are present, raising exceptions for missing datasets.
* **Inputs**: Validated Lead Profile, Website Audit Report, Prototype Report, Contact Information, Configuration settings.
* **Outputs**: `UnifiedInputPackage` dictionary.

#### 2.2 Context Builder
* **Purpose**: Aggregate multiple raw details into a single cohesive context block.
* **Responsibilities**:
  - Merge lead, audit, scoring, and prototype data.
  - Deduplicate redundant records.
  - Normalize text strings and categories.
* **Inputs**: `UnifiedInputPackage`
* **Outputs**: `UnifiedBusinessContext` dictionary.

#### 2.3 Personalization Manager
* **Purpose**: Filter the context to select specific personalization hook parameters.
* **Responsibilities**:
  - Identify target company name and role.
  - Select industry-specific terminology.
  - Select high-impact modernization opportunities based on the audit.
* **Inputs**: `UnifiedBusinessContext`
* **Outputs**: `PersonalizationContext` dictionary.

#### 2.4 Prompt Builder
* **Purpose**: Map personalization hooks into target instruction templates.
* **Responsibilities**:
  - Insert context elements into prompt structures.
  - Apply agency writing instructions (formal tone, upgrade benefits).
  - output a strongly typed prompt package.
* **Inputs**: `PersonalizationContext`
* **Outputs**: `AIPromptPackage` dictionary.

#### 2.5 AI Generation Manager
* **Purpose**: Call the generation client to draft the personalized email.
* **Responsibilities**:
  - Generate email subject line.
  - Draft body sections detailing prototype highlights.
  - Include CTA and professional closing.
* **Inputs**: `AIPromptPackage`
* **Outputs**: `GeneratedEmail` dictionary (contains subject and body draft).

#### 2.6 Email Validator
* **Purpose**: Verify generated text matches quality criteria.
* **Responsibilities**:
  - Ensure all required sections are present.
  - Scan and block empty template placeholders (e.g. `[Name]`, `{Domain}`).
  - Evaluate formatting, tone, and length constraints.
* **Inputs**: `GeneratedEmail`
* **Outputs**: `ValidatedEmail` dictionary, `ValidationReport` details.

#### 2.7 Output Formatter
* **Purpose**: Apply structural layouts to validated email drafts.
* **Responsibilities**:
  - Convert text drafts into HTML formats.
  - Normalize spacing, list tags, and alignment.
* **Inputs**: `ValidatedEmail`
* **Outputs**: `FormattedEmailPackage` dictionary (contains HTML payload).

#### 2.8 Metadata Generator
* **Purpose**: Append tracking metadata to the final deliverable package.
* **Responsibilities**:
  - Generate a unique execution UUID.
  - Record execution timestamp and engine version.
  - Merge metadata with formatted email package.
* **Inputs**: `FormattedEmailPackage`, `ValidationReport`
* **Outputs**: `MetadataPackage` dictionary, `FinalEmailPackage` dictionary.

---

### 3. Module Independence & Execution Control
* **Fixed Sequence**: Execution must follow the strict pipeline order.
* **Failure Propagation**: If any layer returns an error or validation failure, subsequent stages are cancelled immediately, intermediate outputs are discarded, and an failure trace is logged.
