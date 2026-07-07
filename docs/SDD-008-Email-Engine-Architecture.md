# System Design Document (SDD-008)
## Phase 8.1 - AI Personalized Email Engine Architecture

### 1. Overview
The AI Personalized Email Engine is a stateless enterprise service designed to generate and format tailored outreach emails based on upstream intelligence (audits, niches, scoring, contact details, and prototype layouts). 
* **Protocol & Pluggability**: Standard SMTP configuration is implemented as the core transmission layer, allowing custom domain SMTP or Gmail integration via `.env` files. The outbound subsystem is designed as an interface (`IEmailService`), permitting modular expansion to switch to API-based providers (such as Brevo, SendGrid, or Mailgun) without altering upstream workflows.
* **Rich Format Support**: The architecture supports HTML mail formatting out of the box, facilitating rich layouts, inline elements, links, and prototype preview assets.

---

### 2. Architectural Position
The engine acts as a bridge between prototype generation and customer engagement.
```
Prototype Intelligence Engine (Phase 7)
↓
AI Personalized Email Engine (Phase 8) [Current Phase]
↓
Follow-Up Engine (Phase 9) / CRM Engine (Phase 10)
```
Execution begins only after all upstream stages complete successfully and outputs a finalized `Final Email Package`.

---

### 3. Architectural Principles
* **Single Responsibility**: Each sub-module does one thing (e.g., Context Assembly only aggregates, AI Generation only runs prompts).
* **Statelessness**: No persistent execution state is saved locally.
* **Unidirectional Flow**: Data flows strictly sequentially from Input to Output.
* **HTML Capability**: Dedicated formatting layer supports rich text and HTML templates.
* **Provider Decoupling**: Underlying SMTP or API providers are abstracted behind a generic service contract.

---

### 4. High-Level Architecture
```
┌───────────────────────────────────────────────────────────────┐
│                    AI Personalized Email Engine               │
│                                                               │
│  ┌────────────────────────┐       ┌────────────────────────┐  │
│  │   Input Aggregation    │ ────> │    Context Assembly    │  │
│  └────────────────────────┘       └────────────────────────┘  │
│                                               │               │
│                                               ▼               │
│  ┌────────────────────────┐       ┌────────────────────────┐  │
│  │  Prompt Construction   │ <──── │  Personalization Prep  │  │
│  └────────────────────────┘       └────────────────────────┘  │
│               │                                               │
│               ▼                                               │
│  ┌────────────────────────┐       ┌────────────────────────┐  │
│  │   AI Generation Layer  │ ────> │   Output Validation    │  │
│  └────────────────────────┘       └────────────────────────┘  │
│                                               │               │
│                                               ▼               │
│                                   ┌────────────────────────┐  │
│                                   │   Formatting Layer     │  │
│                                   └────────────────────────┘  │
└───────────────────────────────────────────────┬───────────────┘
                                                ▼
                                      Final Email Package
                                 (HTML Body + Metadata + SMTP)
```

---

### 5. Architectural Layers
The engine consists of 7 logical layers:
1. **Input Aggregation Layer**: Resolves and loads data from SQLite tables (`search_leads`, `audits`, `business_profiles`, `lead_scores`, `contacts`, `validated_emails`).
2. **Context Assembly Layer**: Combines domain, speed audit results, niche recommendations, and visual mockups into a structured `Business Context Package`.
3. **Personalization Layer**: Selects appropriate hook variables, company name, industry terminology, and specific prototype highlights.
4. **Prompt Construction Layer**: Injects personalization fields into pre-defined templates to produce the `AI Prompt Package`.
5. **AI Email Generation Layer**: Calls the Gemini API to draft subject lines, email bodies, call-to-actions, and closings.
6. **Output Validation Layer**: Screens the draft against communication standards and filters empty placeholder tags.
7. **Formatting Layer**: Transforms valid raw text drafts into structured HTML payloads conforming to the enterprise design layout, ready for SMTP or API transmission.

---

### 6. Data Flow
```
Validated Inputs
  └─ Audited Leads & Contacts
        │
        ▼
   [Layer 1: Input Aggregation]
        │  (Raw DB inputs)
        ▼
   [Layer 2: Context Assembly]
        │  (Business Context DTO)
        ▼
   [Layer 3: Personalization Layer]
        │  (Personalized Variables DTO)
        ▼
   [Layer 4: Prompt Construction]
        │  (Formatted Prompt Package)
        ▼
   [Layer 5: AI Generation Layer]
        │  (Raw Text Email Draft)
        ▼
   [Layer 6: Output Validation]
        │  (Verified Text Package)
        ▼
   [Layer 7: Formatting Layer]
        │
        ▼
  Final Email Package (HTML Output + Metadata)
```

---

### 7. Upstream Dependencies
* **Search Engine**: Target domain lists.
* **Audit Engine**: Scores, mobile compliance, page speed metrics.
* **Niche Detection**: Target industry classifications.
* **Lead Scoring**: Lead prioritization status.
* **Contact & Email Validation**: Verified outreach email addresses.
* **Prototype Engine**: Preview links, screenshots, and visual upgrade configurations.

---

### 8. Downstream Dependency
* **Follow-Up Engine / SMTP**: Delivers the final HTML email package via port 587/465 (or standard SMTP channel).
* **CRM Engine**: Transitions lead status to `CONTACTED` or `EMAILED` and logs outreach timestamps.

---

### 9. State Management
The execution follows a strict request-response lifecycle:
1. **Init**: Load inputs into memory.
2. **Execution**: Pass the DTO sequentially through the 7 layers.
3. **Writeback**: Commit final package payload and metadata to database.
4. **Clean**: Purge in-memory DTO. No temporary session state is stored.

---

### 10. Failure Handling
* **Missing Upstream Data**: Raise `MandatoryInputMissingException` and transition state to `FAILED`.
* **API/SMTP Timeout**: Retry transient network errors up to 3 times with exponential backoff.
* **Validation Failure**: If the generated content contains placeholders or missing sections, mark the transaction as failed. No partial or corrupted emails will be transmitted or logged.

---

### 11. Scalability Requirements
* **Concurrency**: Thread-safe execution using independent, isolated contexts per lead.
* **Parallel Processing**: Supports concurrent pipeline workers sending emails to distinct clients without database contention.
* **Decoupled Outbound Client**: SMTP service client instantiation is separated from generation logic to allow independent connection pooling.

---

### 12. Security Principles
* **Credential Protection**: Hardcoded credentials are strictly banned. Credentials (SMTP user, password, server, port, API keys) must be loaded from `.env` files.
* **Data Isolation**: Execution processes cannot modify upstream tables.
* **Content Sanitization**: Output formatting sanitizes HTML entities to prevent remote code execution or script injection inside outbound mail clients.
