# Software Design Document: SDD-003
## Website Audit Engine Design Specification

* **Document Version**: 2.1.0 (LOCKED Architecture Spec)
* **Status**: APPROVED & LOCKED
* **Author**: Enterprise Software Architect
* **Target Phase**: Phase 2 — Website Audit Engine

---

### 1. Purpose
The purpose of the Website Audit Engine is to automatically inspect and diagnose the website quality of business leads discovered during Phase 1. It crawls targets to identify critical technical deficits (such as lack of SSL, poor mobile viewport responsiveness, slow loading speeds, and missing SEO optimization) that can be leveraged during automated outreach campaigns.

---

### 2. Objectives
* Quantify website technical and structural quality across 5 main categories: SEO, Mobile, Speed, Trust, and Design.
* Store normalized metrics in a relational database mapping audits to unique lead profiles.
* Generate a structured JSON payload for downstream intake.
* Run audits with zero manual intervention.

---

### 3. Scope
* **In-Scope**:
  * Homepage crawling (redirect resolution, HTML parsing, DOM examination).
  * SSL connection handshake parsing.
  * Timing-to-first-byte (TTFB) and overall load calculations.
  * Score calculation logic and persistence to the database.
* **Out-of-Scope**:
  * Crawling multiple subpages (limited to homepage only).
  * AI prototype generation or site modernization suggestions.
  * CRM integrations, email generation, or delivery workflows.

---

### 4. Responsibilities
* **AuditAgent**: Main coordinator responsible for pulling lead tasks, running crawl routines, executing rules calculations, committing database transactions, and publishing event completions.
* **AuditService**: Low-level networking and page retrieval worker. Handles TCP SSL connections, browser engine launches, and raw HTML extractions.
* **AuditRules**: The scoring calculator. Consumes raw parsed data and computes category/overall scores based on EDK specifications.
* **Database Engine**: Stores persistent audit records.
* **Redis Manager**: Manages queue tasks ingestion and enqueues tasks for downstream modules (e.g. niche detection).

---

### 5. Architecture & Sequence Diagrams

#### 5.1 System Data Flow
```
              [Redis Queue: audit_queue]
                         │
                         ▼ (lead_id, domain)
                  [Master Agent]
                         │
                         ▼
                   [AuditAgent]
                         │
        ┌────────────────┴────────────────┐
        ▼ (Playwright / HTTP Get)          ▼ (Socket TCP Handshake)
  [AuditService: Page Fetch]      [AuditService: Certificate Check]
        │                                 │
        └────────────────┬────────────────┘
                         ▼ (Parsed Signals)
                  [AuditRules]
                         │
                         ▼ (Scores & Summary)
                [Database: audits]
                         │
                         ▼ (Publish Completion)
           [Redis Queue: niche_queue]
```

#### 5.2 Sequence Diagram Verification
The step-by-step lifecycle of a lead audit run is documented in the sequence flowchart below:

```
[Queue Mgr]  [AuditAgent]   [BrowserEngine]   [RulesEngine]   [Database]    [Event Bus]
     │            │                │                │              │             │
     │──(Task)───►│                │              │             │
     │            │                │                │              │             │
     │            │──(Fetch URL)──►│                │              │             │
     │            │◄─(HTML/Timings)│                │              │             │
     │            │                                 │              │             │
     │            │──(Evaluate Category Strategies)►│              │             │
     │            │◄─(Calculated Scores)────────────│              │             │
     │            │                                                │             │
     │            │──(Write Audit transaction)────────────────────►│             │
     │            │◄─(Commit Success)──────────────────────────────│             │
     │            │                                                              │
     │            │──(Publish audit_completed Event)────────────────────────────►│
```

---

### 6. Execution Workflow
1. **Intake**: The orchestrator receives a task payload `{"lead_id": 1, "domain": "example.com"}` from the Redis `audit_queue`.
2. **Duplicity Check**: Agent checks the `audits` table. If an audit already exists, the task is skipped to prevent redundant crawling.
3. **Crawl Phase**:
   * AuditService initiates a secure SSL socket query to verify certificate presence, issuer, and expiration date.
   * AuditService launches the active `IBrowserEngine` subclass to fetch the homepage HTML and measure TTFB and DOM load timings.
4. **Scoring Phase**: AuditRules parses the collected metrics and HTML tags through concrete instances of `IAuditScoreStrategy` to calculate scores for SEO, Mobile, Speed, Trust, and Design.
5. **Database Transaction**:
   * Opens an active database transaction.
   * Inserts the metrics record into the `audits` table.
   * Updates the `search_leads` record status column to `AUDITED`.
   * Commits the transaction.
6. **Task Transition**: Push the domain payload to the downstream queue (`niche_queue`).
7. **Event Notification**: Publishes an `audit_completed` event to the system Event Bus.

---

### 7. Module Specifications

#### 7.1 `agents/audit/audit_models.py`
Defines the SQLAlchemy model representing the database schema.
* Extends `Base` declarative engine model.
* Defines primary and foreign key constraints.

#### 7.2 `agents/audit/audit_services.py`
Contains network query operations and the browser engine abstractions.
* Utilizes python `socket` and `ssl` modules for certificate handshakes.
* Integrates `IBrowserEngine` interface for page loaders.

#### 7.3 `agents/audit/audit_rules.py`
Processes HTML string outputs using concrete scoring strategies:
* Implements Strategy pattern for score calculations.
* Aggregates calculations and maps rules to `schema_version` and `audit_rule_version` parameters.

#### 7.4 `agents/audit/audit_agent.py`
Binds services, rules, and database engines under a single coordinator loop.

---

### 8. Interface Contracts
All components conform to these defined abstract class contracts:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class IBrowserEngine(ABC):
    @abstractmethod
    async def fetch_url(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Launches the browser instance, loads the page, and extracts HTML & network statistics.
        
        Returns:
            Dict containing "html", "load_time_ms", "response_time_ms", and "headers".
        """
        pass

class IAuditScoreStrategy(ABC):
    @abstractmethod
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        """
        Evaluates a specific category of web vitals/elements and returns a score out of 100.
        """
        pass

class IAuditAgent(ABC):
    @abstractmethod
    async def audit_site(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Runs the database checking, crawling, scoring, persistence,
        and downstream queue notification workflow.
        """
        pass

class IAuditService(ABC):
    @abstractmethod
    async def fetch_page_content(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Establishes socket SSL connections and invokes the browser abstraction engine.
        """
        pass

class IAuditRules(ABC):
    @abstractmethod
    def calculate_scores(self, parse_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates category scores using strategies, computes overall score, and generates a summary.
        """
        pass
```

---

### 9. Input/Output Contracts

#### 9.1 Input Contract
* **Format**: JSON / Dict
* **Schema**:
  ```json
  {
    "lead_id": int,
    "domain": str
  }
  ```

#### 9.2 Output Contract
* **Format**: JSON / Dict
* **Schema**:
  ```json
  {
    "lead_id": int,
    "domain": str,
    "schema_version": str,
    "audit_rule_version": str,
    "audit_score": int,
    "metrics": {
      "seo": { "score": int, "title_present": bool, "meta_description_present": bool, "h1_count": int },
      "mobile": { "score": int, "has_viewport": bool, "responsive_layout_detected": bool },
      "speed": { "score": int, "response_time_ms": int, "load_time_ms": int },
      "trust": { "score": int, "ssl_valid": bool, "ssl_issuer": str, "privacy_policy_present": bool, "contact_info_present": bool },
      "design": { "score": int, "cta_buttons_detected": bool }
    },
    "summary": str,
    "timestamp": str
  }
  ```

---

### 10. Audit JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AuditPayload",
  "type": "object",
  "properties": {
    "lead_id": { "type": "integer" },
    "domain": { "type": "string" },
    "schema_version": { "type": "string" },
    "audit_rule_version": { "type": "string" },
    "audit_score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "metrics": {
      "type": "object",
      "properties": {
        "seo": {
          "type": "object",
          "properties": {
            "score": { "type": "integer" },
            "title_present": { "type": "boolean" },
            "meta_description_present": { "type": "boolean" },
            "h1_count": { "type": "integer" }
          },
          "required": ["score", "title_present", "meta_description_present", "h1_count"]
        },
        "mobile": {
          "type": "object",
          "properties": {
            "score": { "type": "integer" },
            "has_viewport": { "type": "boolean" },
            "responsive_layout_detected": { "type": "boolean" }
          },
          "required": ["score", "has_viewport", "responsive_layout_detected"]
        },
        "speed": {
          "type": "object",
          "properties": {
            "score": { "type": "integer" },
            "response_time_ms": { "type": "integer" },
            "load_time_ms": { "type": "integer" }
          },
          "required": ["score", "response_time_ms", "load_time_ms"]
        },
        "trust": {
          "type": "object",
          "properties": {
            "score": { "type": "integer" },
            "ssl_valid": { "type": "boolean" },
            "ssl_issuer": { "type": "string" },
            "privacy_policy_present": { "type": "boolean" },
            "contact_info_present": { "type": "boolean" }
          },
          "required": ["score", "ssl_valid", "ssl_issuer", "privacy_policy_present", "contact_info_present"]
        },
        "design": {
          "type": "object",
          "properties": {
            "score": { "type": "integer" },
            "cta_buttons_detected": { "type": "boolean" }
          },
          "required": ["score", "cta_buttons_detected"]
        }
      },
      "required": ["seo", "mobile", "speed", "trust", "design"]
    },
    "summary": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "lead_id", 
    "domain", 
    "schema_version",
    "audit_rule_version",
    "audit_score", 
    "metrics", 
    "summary", 
    "timestamp"
  ]
}
```

---

### 11. Database Schema
```sql
CREATE TABLE audits (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER UNIQUE NOT NULL,
    schema_version VARCHAR(10) NOT NULL,
    audit_rule_version VARCHAR(10) NOT NULL,
    audit_score INTEGER NOT NULL,
    seo_score INTEGER NOT NULL,
    mobile_score INTEGER NOT NULL,
    speed_score INTEGER NOT NULL,
    trust_score INTEGER NOT NULL,
    design_score INTEGER NOT NULL,
    summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES search_leads(id) ON DELETE CASCADE
);

CREATE INDEX idx_audits_lead_id ON audits(lead_id);
```

---

### 12. Scoring Matrix (Strategy Pattern Configuration)
The overall score is computed out of 100 using a weighted formula:

$$\text{Overall Score} = 0.25 \times \text{Speed} + 0.20 \times \text{SEO} + 0.20 \times \text{Mobile} + 0.20 \times \text{Trust} + 0.15 \times \text{Design}$$

The calculation is delegated to specific strategy classes implementing `IAuditScoreStrategy`.

#### 12.1 `SeoScoreStrategy` (100 pts)
* `<title>` presence: +30 pts (length checks: must be between 10-60 characters, otherwise +15 pts).
* `<meta name="description">` presence: +30 pts.
* Single `<h1>` tag presence: +20 pts (reduced to +10 pts if $0$ or $>1$ exist).
* Presence of structural subheadings (`<h2>`/`<h3>`): +20 pts.

#### 12.2 `MobileScoreStrategy` (100 pts)
* Meta viewport tag found: +60 pts.
* Responsive CSS design patterns (Grid, `@media`, Flex) present: +40 pts.

#### 12.3 `SpeedScoreStrategy` (100 pts)
* First-byte response time (TTFB) $< 500\text{ms}$: 100 pts.
* TTFB $500\text{ms} - 1.5\text{s}$: 75 pts.
* TTFB $1.5\text{s} - 3.0\text{s}$: 50 pts.
* TTFB $> 3.0\text{s}$: 25 pts.

#### 12.4 `TrustScoreStrategy` (100 pts)
* Valid SSL certificate configuration: +40 pts.
* Privacy Policy or Terms page link detected: +40 pts.
* Business contact parameters (phone / location / email) detected: +20 pts.

#### 12.5 `DesignScoreStrategy` (100 pts)
* Calls-To-Action (CTAs) buttons/links detected: +50 pts.
* Structured HTML tags (header, main, footer) detected: +50 pts.

---

### 13. Configuration Specification
Settings are managed in `config/config.py` and loaded dynamically:

| Config Key | Type | Default | Description |
| --- | --- | --- | --- |
| `AUDIT_CRAWL_TIMEOUT` | Float | `15.0` | HTTP fetch/load connection timeout in seconds. |
| `AUDIT_USER_AGENT` | String | `EDK-AuditAgent/1.0` | Crawler request identity header. |
| `AUDIT_MAX_RETRIES` | Integer | `3` | Maximum retry attempts for transient network blocks. |
| `AUDIT_RETRY_DELAY` | Integer | `5` | Wait time in seconds between retry failures. |

---

### 14. Failure Handling
* **DNS Resolution Failure**: If domain DNS records do not resolve, record a fail-state inside the audit, log a warning, and write an audit score of `0` with the summary `"Domain DNS failed to resolve."`
* **Crawl Timeout / 404 / 500**: Capture HTTP errors. Populate speed metrics with `0` score, but parse response headers if available.
* **SSL Validation Failure**: If SSL certificate handshakes crash, record `ssl_valid = False` and set trust sub-points to `0`, but proceed with basic HTML scraping.
* **Empty HTML Payload**: If content is missing, write scores of `0` for SEO, Mobile, and Design.

---

### 15. Retry Strategy
* **Transient Networks Errors**: For HTTP 503, connection drops, or timeouts, the AuditAgent retries execution up to `AUDIT_MAX_RETRIES` times.
* **Backoff Policy**: Delays between retries follow an exponential backoff formula:

$$\text{Delay} = \text{AUDIT\_RETRY\_DELAY} \times 2^{\text{attempt}}$$

* **Final Failure**: If all retries fail, update the lead status to `FAILED_AUDIT` in the database, write an error log, and release the task from memory without enqueuing it downstream.

---

### 16. Security Requirements
* **Command & Input Sanitization**: URLs are parsed through `urllib.parse` before socket/browser executions.
* **Sandbox Browser execution**: Headless browsers run with sandbox parameters enabled (`--no-sandbox` only when running inside containerized testing engines).
* **Regex Bounded Search**: Text parsing algorithms use non-backtracking regular expressions to avoid ReDoS security exploits.

---

### 17. Logging Requirements
* **Format**: JSON logging output.
* **Parameters**: Every log must include a correlation ID.
* **Example Log Trace**:
  `{"timestamp": "2026-07-05T08:11:00.123Z", "level": "INFO", "module": "audit_agent", "message": "Starting audit crawl for lead ID 101 on domain example.com", "correlation_id": "REQ-101-ABC"}`

---

### 18. Performance Targets
* **Maximum Crawl Duration**: Individual crawler execution time limit of 15 seconds.
* **Average Database Latency**: Database read and write transaction completion time $\le 15\text{ms}$.
* **Resource Leaks**: Headless browser contexts are closed programmatically after every execution run.

---

### 19. Testing Strategy
* **Isolated Unit Checks**: Mock parser classes using mock HTML responses to verify the scoring logic.
* **Integration Database Tests**: Use an in-memory SQLite database to run queries, test foreign key integrity, and verify duplicate checks.
* **Scraper Fallback Checks**: Force connection timeouts during test runs to verify that the system gracefully executes the `aiohttp` fallback scraper.

---

### 20. PASS Conditions
* **Target Audited Successfully**: Site crawled and structured metrics written to `audits` table.
* **Leads Transition**: Lead record status updated to `AUDITED`.
* **Tests Passed**: 100% passes on all suite runs.
* **Exit Checklist**: All EDK checklist gates signed off.

---

### 21. FAIL Conditions
* Database schema creation failures or session transaction rollbacks.
* Loop execution blockages caused by missing timeouts.
* Unhandled exception crashes propagating up to the Master Agent loop.

---

### 22. Phase Exit Checklist
Checklist matches [docs/PEC-003-Phase-2-Exit-Checklist.md](file:///c:/Users/user/Desktop/WEBSITE%20%20AGENCY/docs/PEC-003-Phase-2-Exit-Checklist.md).

---

### 23. LOCK Conditions
* **Code Freeze**: Post-approval, `audit_models.py`, `audit_agent.py`, `audit_services.py`, and `audit_rules.py` are frozen.
* **Audit Approval**: Verification metrics verified by the QA Auditor.
