# Interface Contracts: IC-003
## Phase 2 - Website Audit Engine Interface Specifications

This document defines the strict interface contracts, class signatures, method parameters, and JSON schemas for all modules implemented in **Phase 2: Website Audit Engine**.

---

### 1. Browser Engine Abstraction: `IBrowserEngine`
Defines the connection layer interface used by page loading services.

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class IBrowserEngine(ABC):
    @abstractmethod
    async def fetch_url(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Launches the browser instance, loads the page, and extracts HTML & network statistics.
        
        Args:
            url: Target URL to fetch.
            timeout: Max fetch time in seconds.
            
        Returns:
            Dict containing:
                - "html": Raw HTML page source code string.
                - "load_time_ms": Duration to reach loaded state in ms.
                - "response_time_ms": Response start delay (TTFB) in ms.
                - "headers": Dict of HTTP response headers.
        """
        pass
```

---

### 2. Rules Evaluation Strategy: `IAuditScoreStrategy`
Implements the Strategy pattern for auditing sub-categories.

```python
class IAuditScoreStrategy(ABC):
    @abstractmethod
    def evaluate(self, page_data: Dict[str, Any]) -> int:
        """
        Evaluates a specific category of web vitals/elements and returns a score out of 100.
        
        Args:
            page_data: Output dictionary containing parsed HTML source and timings.
            
        Returns:
            Integer score from 0 to 100.
        """
        pass
```

---

### 3. Agent Orchestrator: `AuditAgent`
The AuditAgent listens to tasks and manages the audit lifecycle.

```python
class IAuditAgent(ABC):
    @abstractmethod
    async def audit_site(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Main orchestration method:
        1. Query database to verify lead_id exists and status is 'DISCOVERED'.
        2. Invoke AuditService to fetch and parse target homepage.
        3. Invoke AuditRules to calculate scores using scoring strategies.
        4. Write audit metrics into the 'audits' table in a single database transaction.
        5. Update the 'search_leads' table record status to 'AUDITED'.
        6. Return EDK-compliant structured report dict.
        
        Args:
            lead_id: Unique integer index of target lead in search_leads.
            url: Target domain/URL string.
            
        Returns:
            Dict containing the audit score details.
            
        Raises:
            ValueError: If lead_id not found or status invalid.
            Exception: On network or database write failures (triggers transaction rollback).
        """
        pass
```

---

### 4. Crawling Service: `AuditService`
The crawling service handles low-level HTTP requests and page rendering.

```python
class IAuditService(ABC):
    @abstractmethod
    async def fetch_page_content(self, url: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Establishes socket SSL connections and invokes the browser abstraction engine.
        
        Args:
            url: Target URL to crawl.
            timeout: Maximum connection timeout in seconds.
            
        Returns:
            Dict containing:
                - "html": HTML body string.
                - "load_time_ms": Page load time in milliseconds.
                - "response_time_ms": Time-to-first-byte (TTFB) in milliseconds.
                - "ssl_valid": Boolean indicating certificate validity.
                - "ssl_issuer": Common Name (CN) string of CA.
                - "ssl_expiry": Expiration datetime string.
                - "headers": HTTP response headers dict.
        """
        pass
```

---

### 5. Rules Engine: `AuditRules`
The rules engine converts raw HTML and network parameters into normalized scores.

```python
class IAuditRules(ABC):
    @abstractmethod
    def calculate_scores(self, parse_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes scoring logic matrices defined in SDD-003 using strategies.
        
        Args:
            parse_payload: Output dictionary from AuditService.fetch_page_content.
            
        Returns:
            Dict containing:
                - "seo_score": Integer (0-100)
                - "mobile_score": Integer (0-100)
                - "speed_score": Integer (0-100)
                - "trust_score": Integer (0-100)
                - "design_score": Integer (0-100)
                - "audit_score": Weighted integer (0-100)
                - "schema_version": Schema configuration tag string
                - "audit_rule_version": Rules engine code tag string
                - "summary": Short descriptive text.
        """
        pass
```

---

### 6. JSON Serialization Output Contract
The final audit result exported from the agent or database query must conform to the following schema structure:

```json
{
  "lead_id": 123,
  "domain": "target-niche-clinic.com",
  "schema_version": "1.0.0",
  "audit_rule_version": "1.0.0",
  "audit_score": 78,
  "metrics": {
    "seo": {
      "score": 85,
      "title_present": true,
      "meta_description_present": false,
      "h1_count": 1,
      "headings_hierarchy_ok": true
    },
    "mobile": {
      "score": 100,
      "has_viewport": true,
      "responsive_layout_detected": true
    },
    "speed": {
      "score": 75,
      "response_time_ms": 320,
      "load_time_ms": 1240
    },
    "trust": {
      "score": 60,
      "ssl_valid": true,
      "ssl_issuer": "Let's Encrypt",
      "privacy_policy_present": true,
      "terms_of_service_present": false,
      "contact_info_present": true,
      "social_links": ["https://facebook.com/nicheclinic"]
    },
    "design": {
      "score": 70,
      "cta_buttons_detected": true,
      "structural_tags_detected": true
    }
  },
  "summary": "Website has active SSL and mobile responsiveness, but lacks meta description and terms of service pages.",
  "timestamp": "2026-07-05T08:11:00Z"
}
```
