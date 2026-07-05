# Software Architecture Specification (SAS)
## AI Website Upgrade Agency - Project Constitution, Vision & Architecture

### Document Details
* **Document Number**: SAS-001
* **Version**: 1.0.0
* **Status**: IN_REVIEW
* **Date**: 2026-07-05

---

### 1. Purpose
This document establishes the foundational architectural constitution, system vision, business goals, and high-level component structure for the AI Website Upgrade Agency platform. It serves as the baseline for all subsequent design and implementation documents.

---

### 2. Objectives
* **1. Automation**: Achieve 100% autonomous client acquisition pipeline execution.
* **2. Conversion**: Leverage tailored AI-generated website prototypes to maximize sales outreach conversions.
* **3. Modularity**: Enforce complete separation of concerns and independent component replacement.
* **4. Cost Efficiency**: Minimize large language model (LLM) token consumption via deterministic rules and local processing.
* **5. Scalability**: Design for future SaaS transition, supporting concurrent operations across multiple niches.

---

### 3. Scope
#### 3.1 In-Scope (Version 1.0)
* Autonomous business prospecting and website auditing.
* Automated niche detection and lead scoring.
* Playwright-driven contact extraction and validation.
* AI-driven HTML prototype generation.
* Automated email outreach and CRM tracking.
* Daily operational status reports and Telegram notifications.

#### 3.2 Out-of-Scope (Version 1.0)
* Voice calling integrations.
* Client billing and payment gateways.
* Multi-user team collaboration.
* Native mobile applications.
* Client portal or authentication systems.

---

### 4. Responsibilities
* **Desktop Dashboard**: Renders system status, lead metrics, logs, and manual overrides.
* **Master Agent**: Orchestrates overall process execution, handles task dispatching, error recovery, and status tracking.
* **Workflow Engine**: Executes the pipeline sequences, enforcing sequential transitions and dependencies.
* **Search Agent**: Queries data sources to discover businesses matching outdated website criteria.
* **Website Audit Agent**: Runs remote performance and layout analysis on identified business websites.
* **Niche Detection Agent**: Identifies specific service categories and design strategies based on audit data.
* **Lead Scoring Agent**: Ranks leads based on upgrade potential and validation.
* **Contact Extraction Agent**: Gathers phone numbers, social media links, and emails.
* **Email Validation Agent**: Filters invalid and bouncing emails.
* **AI Prototype Generator**: Generates premium static HTML/CSS layout redesigns.
* **AI Email Engine**: Crafts personalized sales emails using audit insights.
* **Follow-Up Engine**: Tracks intervals and manages reminder email campaigns.
* **CRM Engine**: Manages pipeline states (e.g., Lead, Audited, Emailed, Converted).
* **Telegram Reporter**: Dispatches daily alerts and system failures.

---

### 5. Inputs
* **Target Criteria**: Industry niches, geographic targets, search keywords.
* **Configuration Parameters**: API keys, database credentials, model temperature, scraping delay.
* **Raw Web Content**: Scraping data, website source code, CSS selectors, DNS records.

---

### 6. Outputs
* **Audit Reports**: Structured JSON and Markdown documents containing website scoring metrics.
* **Tailored HTML Prototypes**: Responsive mockups using curated color palettes (HSL).
* **Outreach Templates**: Customized email bodies for target clients.
* **CRM Records**: Updated lead details, contact status, and interaction history.
* **System Reports**: Operational summaries and error logs sent to Telegram.

---

### 7. Workflow
The operational workflow proceeds sequentially as follows:

Search Agent
↓
Website Audit Agent
↓
Niche Detection Agent
↓
Lead Scoring Agent
↓
Contact Extraction Agent
↓
Email Validation Agent
↓
AI Prototype Generator
↓
AI Email Engine
↓
Follow-Up Engine
↓
CRM Engine
↓
Telegram Reporter

---

### 8. Execution Flow
1. **Initiation**: Desktop Dashboard sends a start signal containing target search criteria.
2. **Master Agent Initialization**: Loads global configuration and schedules workflow runs.
3. **Queue Enqueue**: Master Agent adds search task to Queue Manager.
4. **Agent Execution**:
   * Search Agent queries search engines and appends target URLs to Database.
   * Website Audit Agent crawls target websites using Playwright, analyzing structural indicators.
   * Niche Detection Agent processes raw page content, classifying business category.
   * Lead Scoring Agent calculates upgrade score.
   * Contact Extraction Agent retrieves contact records.
   * Email Validation Agent filters verified addresses.
   * AI Prototype Generator creates visual redesign and stores prototype files.
   * AI Email Engine structures custom draft.
   * CRM Engine logs outreach timestamp and moves state to "CONTACTED".
5. **Reporting**: Daily Telegram alert containing pipeline KPIs is compiled and sent.

---

### 9. Architecture
* **Clean Architecture**: Decouples business rules from database, framework, and UI.
* **SOLID**: Ensured by strict interface boundaries and single-responsibility classes.
* **Dependency Injection (DI)**: Components request dependencies (e.g., DB repository, API clients) via constructor injection.
* **Loose Coupling**: Subsystems communicate strictly via structured DTOs and abstract interfaces.
* **Token Optimization Rule**:
  Rule-based logic
  ↓
  Local Processing
  ↓
  AI Reasoning
  ↓
  Large Model Calls

---

### 10. Components
```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│   ┌──────────────────────┐    ┌────────────────────┐   │
│   │  Desktop Dashboard   │    │  Admin Dashboard   │   │
│   └──────────────────────┘    └────────────────────┘   │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                  Business Logic Layer                  │
│                ┌──────────────────────┐                │
│                │     Master Agent     │                │
│                └──────────┬───────────┘                │
│                           ▼                            │
│   ┌────────────────────────────────────────────────┐   │
│   │                Workflow Engine                 │   │
│   └──────┬───────────────┬──────────────────┬──────┘   │
│          ▼               ▼                  ▼          │
│   ┌─────────────┐ ┌─────────────┐    ┌─────────────┐   │
│   │Search Agent │ │ Audit Agent │    │ Email Agent │   │
│   └─────────────┘ └─────────────┘    └─────────────┘   │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                  │
│   ┌─────────────┐ ┌─────────────┐    ┌─────────────┐   │
│   │ PostgreSQL  │ │    Redis    │    │ Playwright  │   │
│   └─────────────┘ └─────────────┘    └─────────────┘   │
└────────────────────────────────────────────────────────┘
```

---

### 11. Interfaces
* **`ISearchAgent`**: Methods for querying search APIs or web directories.
* **`IAuditAgent`**: Methods to parse target sites and output performance scores.
* **`IPrototypeGenerator`**: Methods to accept business profiles and generate HTML templates.
* **`IEmailService`**: Methods for validating address domains and sending outbox messages.
* **`IDatabaseRepository`**: Methods for ACID-compliant persistence.

---

### 12. Validation Rules
* **Configuration Integrity**: Validate that all API keys, database connection URIs, and credentials are set in the environment before any agent runs.
* **Input URL Validation**: Verify syntax and reachability of target domains.
* **Email Validation**: Enforce strict syntax checks and domain MX record validations.
* **AI Output Schemas**: Force all AI generator outputs to match Pydantic schemas.

---

### 13. Failure Handling
* **Retry Protocol**: Retry transient API failures up to 3 times with exponential backoff.
* **Circuit Breakers**: Halt connection attempts to downstream APIs (e.g., Gemini) if error rates exceed 20% in a 5-minute window.
* **Database Transactions**: Roll back CRM state changes if email sending fails completely.

---

### 14. Constraints
* **Language**: Python 3.11+.
* **Database**: PostgreSQL (relational storage), Redis (queue and cache).
* **Framework**: FastAPI (asynchronous execution).
* **LLM Engine**: Gemini API.
* **UI styling**: Output prototypes must use vanilla CSS with HSL colors and modern fonts. No template placeholders allowed.

---

### 15. Performance Requirements
* **Concurrency**: Search and Audit agents must operate concurrently up to 10 threads.
* **Audit Duration**: Maximum 60 seconds per website.
* **DB Connection Pool**: Minimum 20 persistent connections.
* **Response Latency**: FastAPI endpoints must return within 200ms.

---

### 16. Security Rules
* **Credential Protection**: Absolute ban on hardcoded API keys. Access credentials via `.env` or system environment.
* **Sandbox Execution**: Run Playwright in sandboxed environments to mitigate remote code execution (RCE) vectors from untrusted websites.
* **Database Access**: Bind PostgreSQL queries strictly through parameterized statements.

---

### 17. Logging Requirements
* **Format**: Structured JSON logging.
* **Target**: Stdout and local log files.
* **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL.
* **Correlation ID**: Generate a UUID per pipeline run, passing it through every agent.

---

### 18. Configuration
Configuration parameters must be structured in `config.py` using Pydantic Settings.
Key sections:
* `DATABASE_URL`: Connection string for PostgreSQL.
* `REDIS_URL`: Connection string for Redis.
* `GEMINI_API_KEY`: API key for model reasoning.
* `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: Bot communication details.

---

### 19. Testing Requirements
* **Unit Testing**: 90%+ code coverage on Workflow Engine and utility modules using `pytest`.
* **Integration Testing**: End-to-end tests mocking the LLM response to verify data persistence and email triggers.
* **Validation Testing**: Validation of generated HTML layouts against semantic standards.

---

### 20. Audit Requirements
* Trace and record every API token usage action.
* Log all outgoing outreach emails along with recipient domain and timestamp in the database.
* Keep detailed records of target business selections and corresponding scoring matrices.

---

### 21. PASS Conditions
* Search, audit, generation, and dispatch execute without unhandled exceptions.
* Generated HTML is responsive and valid.
* Target database contains populated lead and interaction histories.

---

### 22. FAIL Conditions
* Database connection failure at initialization.
* Missing API key configurations.
* Failure to store pipeline output.

---

### 23. LOCK Conditions
* Once this document is marked as APPROVED, modifications require a formal revision request.
* No code modification in dependent components is allowed without updating this reference.

---

### 24. Summary
This specification defines the structural constitution and design boundaries of the AI Website Upgrade Agency. The platform utilizes a Master Agent orchestrating modular, decoupled sub-agents executing sequentially to drive client acquisition.

---

### 25. Next Document
* **SAS-002**: Master Agent & Workflow Engine Specifications.

---

### DOCUMENT STATUS
* **Current Status**: APPROVED
* **Next Document**: SAS-002

### END OF DOCUMENT
