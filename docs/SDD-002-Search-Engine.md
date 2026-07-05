# Software Design Document (SDD)
## Phase 1 - Search Engine Design Specification

### Document Details
* **Document Number**: SDD-002
* **Version**: 1.0.0
* **Status**: IN_REVIEW
* **Date**: 2026-07-05

---

### 1. Purpose
This document details the software design, database schemas, interfaces, filter validation rules, and testing strategies for Phase 1 (Search Engine). It defines how the system automatically discovers business websites for targeting while filtering out invalid and non-convertible domains.

---

### 2. Objectives
* **1. High-Precision Discovery**: Locate and store business web domains belonging to targeted industries (e.g., Coaching, Schools, Hospitals).
* **2. Domain Sanitization**: Filter out social media platforms, directory aggregators, and malformed URLs.
* **3. Deduplication**: Maintain absolute uniqueness of domains in the lead database.
* **4. Scale**: Discover and store a minimum of 50 unique target domains per execution cycle.

---

### 3. Scope
#### 3.1 In-Scope (Phase 1)
* Implementation of the `SearchAgent` sub-component.
* Scraping engine query integration (Google Search/DuckDuckGo scraper wrapper).
* PostgreSQL database tables and ORM schemas for lead tracking (`search_leads`).
* Domain parsers to strip subpages and subdomains, returning only normalized root domains.
* Blacklisting rules for common directory and social sites (e.g., Yelp, LinkedIn, Facebook).
* Search queue integration with Redis.

#### 3.2 Out-of-Scope (Phase 1)
* Performing audits on target sites (SSL, page speed, mobile checks).
* Classifying business niche or applying visual design generators.
* Sending emails or initiating CRM tracking lifecycles.

---

### 4. Responsibilities
* **Search Agent**: Coordinates query building, scraper execution, database persistence, and Redis queuing.
* **Domain Normalizer**: Extracts the clean root domain from raw URLs (e.g., `https://sub.domain.com/page?q=1` → `domain.com`).
* **Domain Filter Engine**: Compares target domain against validation blacklists and syntax checks.
* **Search Database Repository**: Handles CRUD queries for lead insertion, duplicate checks, and status changes.

---

### 5. Inputs
* **Search Target Profiles**: List of target niches (e.g., `Book Publishers`, `NGOs`), geographic regions, and query keywords.
* **Search Configurations**: API limits, pagination counts, request delays.

---

### 6. Outputs
* **`search_leads` Records**: New entries stored in the PostgreSQL database with status `DISCOVERED`.
* **Redis Task Payloads**: Domain items pushed to the `audit_queue` for downstream consumption by the Audit Agent.
* **Phase Audit Report**: Standard JSON log summarizing discovery counts, duplicates discarded, and blacklisted domains skipped.

---

### 7. Workflow
The search process execution sequence:

Load Niches & Geographic target criteria
↓
Query Search Scraper (e.g., DuckDuckGo)
↓
Extract raw URLs
↓
Normalize URLs to root domains
↓
Apply Social & Directory Filter blacklist
↓
Check database for duplicates
↓
Insert unique domains into `search_leads` table
↓
Push target domains to Redis `audit_queue`
↓
Generate Phase 1 Audit Report

---

### 8. Execution Flow
1. **Trigger**: Master Agent pops a task of type `SEARCH` and invokes `SearchAgent.execute(niche, region)`.
2. **Scraper Loop**: Scraper performs queries for specified keywords, obtaining lists of raw links.
3. **Filtering & Normalization**:
   * Strip paths, protocols, and subdomains.
   * If URL is malformed or invalid domain: Skip.
   * If domain exists in directory/social blacklist: Skip.
4. **Database Check**:
   * Query `search_leads` where `domain = normalized_domain`.
   * If database record exists: Skip.
   * If not found: Insert new row into `search_leads` with status `DISCOVERED`.
5. **Queue Push**: Push a task payload containing the new `lead_id` and `domain` to the Redis `audit_queue`.
6. **Audit Check**: Assess counts. If count is $\ge 50$, output SUCCESS audit log.

---

### 9. Architecture
* **Interface-Driven Scraper**: Abstract `ISearchScraper` allows easy swapping from mock mockups to Google API or DuckDuckGo HTML scrapers without touching the agent loop.
* **Repository Pattern**: Abstract database access using a `LeadRepository` layer.
* **Single Responsibility**: `DomainFilter` is strictly decoupled from database persistence or scraping connections.

---

### 10. Components
#### 10.1 Database Schema
```sql
CREATE TABLE search_leads (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) UNIQUE NOT NULL,
    source VARCHAR(100) NOT NULL,
    niche VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'DISCOVERED' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);
```

#### 10.2 Component Files
* `agents/search/search_agent.py` - Core agent orchestrating search flow.
* `agents/search/search_models.py` - SQLAlchemy ORM model definition.
* `agents/search/domain_filter.py` - Logic to normalize domains and filter blacklists.
* `agents/search/scraper_service.py` - Base scraper utility (DuckDuckGo Search wrapper).

---

### 11. Interfaces
```python
class ISearchScraper(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int) -> List[str]: pass

class ILeadRepository(ABC):
    @abstractmethod
    async def add_lead(self, domain: str, niche: str, source: str) -> Optional[int]: pass
    @abstractmethod
    async def check_duplicate(self, domain: str) -> bool: pass
```

---

### 12. Validation Rules
* **Root Domain Extraction**:
  * Input: `https://www.realestate.com/agents/list?id=5`
  * Normalized: `realestate.com`
* **Social and Directory Blacklist**:
  * Skip any domain containing: `facebook.com`, `twitter.com`, `instagram.com`, `linkedin.com`, `yelp.com`, `youtube.com`, `wikipedia.org`, `yellowpages.com`.
* **Lead Target Niches**: Enforce matching against EDK-supported list:
  `['Book Publishers', 'Schools', 'Hospitals', 'Clinics', 'Restaurants', 'Hotels', 'Law Firms', 'Real Estate', 'Travel Agencies', 'Gyms', 'NGOs', 'Coaching Institutes', 'Local Businesses', 'Portfolio Websites', 'E-Commerce']`

---

### 13. Failure Handling
* **API Rate Limits / Captchas**: If the search provider blocks requests, back off for 30 seconds and retry. If block persists, fall back to alternative search provider or notify the admin via log/Telegram.
* **Database Deadlocks**: Retry transaction commits up to 3 times in case of database concurrency contention.
* **Corrupt URL Parsing**: Gracefully log and skip malformed links without throwing unhandled exceptions.

---

### 14. Constraints
* Scrapers must execute with random user agents and request delays (1.0 to 3.0 seconds) to avoid IP blacklisting.
* SQL insertions must utilize database-level `INSERT ... ON CONFLICT DO NOTHING` statements to prevent double-insert race conditions.

---

### 15. Performance Requirements
* Domain normalization and blacklist filtering must execute in under 5ms per domain.
* Scraping query must return a list of links within 10 seconds.
* Lead insertion transaction must complete in under 50ms.

---

### 16. Security Rules
* Parameterize all query values sent to SQLAlchemy repository.
* Filter out domains matching loopback addresses (`127.0.0.1`, `localhost`) to prevent internal network scanning.

---

### 17. Logging Requirements
* Log every unique domain successfully persisted to the database.
* Output structured warnings for scraping blocks or rate limits.
* Log correlation IDs across the search sequence.

---

### 18. Configuration
```env
# Search Agent Configuration variables
SEARCH_LIMIT=100
SCRAPING_DELAY_MIN=1.5
SCRAPING_DELAY_MAX=3.0
```

---

### 19. Testing Requirements
* Mock scrapers must be created to return controlled lists of URLs.
* Test cases must verify:
  1. Correct extraction of root domains.
  2. Rejection of blacklisted domains.
  3. Rejection of duplicate database entries.
  4. Integration tests verifying database record counts and Redis enqueue operations.

---

### 20. Audit Requirements
* Store a count of scanned links versus saved links.
* Record the name of the scraper source used for each discovered domain.

---

### 21. PASS Conditions
* Minimum 50 unique targets verified and stored in the database.
* Zero duplicate domains present in `search_leads` after run.
* All discovered domains successfully enqueued to `audit_queue`.

---

### 22. FAIL Conditions
* Scraper returns 0 results consistently across all queries.
* Database write operations crash.
* Target count is below 50 unique leads at phase completion.

---

### 23. LOCK Conditions
* Once APPROVED, the scraping models and filtering logic are locked.
* Modifications to blacklists must be documented in a revision log.

---

### 24. Summary
Phase 1 implements the prospecting boundary of the agency. By leveraging normalized query scrapers, root domain validators, and deduplication logic, the Search Engine populates the core CRM database with valid leads.

---

### 25. Next Document
* **SDD-003**: Website Audit Engine Design Specification.

---

### DOCUMENT STATUS
* **Current Status**: APPROVED
* **Next Document**: SDD-003

### END OF DOCUMENT
