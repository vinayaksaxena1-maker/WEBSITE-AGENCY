# Software Design Document (SDD)
## Phase 0 - Foundation Framework Specification

### Document Details
* **Document Number**: SDD-001
* **Version**: 1.0.0
* **Status**: IN_REVIEW
* **Date**: 2026-07-05

---

### 1. Purpose
This document specifies the software design, folder structure, interfaces, and execution flow for Phase 0 (Foundation Framework). It establishes the core utility libraries, database connectors, queue managers, and the skeleton orchestration (Master Agent & Event Bus) required for all subsequent business logic agents.

---

### 2. Objectives
* **1. Standardization**: Provide unified logging, configuration loading, and dependency structures.
* **2. Decoupling**: Enforce asynchronous communication via Redis-backed queue managers and an in-memory event bus.
* **3. Resiliency**: Implement robust connection management (PostgreSQL & Redis) with automatic retries.
* **4. Traceability**: Inject a unified transaction and correlation tracking structure into every event payload.

---

### 3. Scope
#### 3.1 In-Scope (Phase 0)
* Base folder structure configuration.
* Environment variable validation and config injection (`config.py`).
* Centralized structured JSON logger (`logger.py`).
* Database connection pooling and health checking (`database.py`).
* Redis manager for queuing and caching (`redis_manager.py`).
* Abstract workflows manager and scheduler base classes.
* Skeleton Event Bus for internal pub-sub communication.
* Initial Master Agent skeleton and Agent Registry.
* Local health monitoring endpoint.

#### 3.2 Out-of-Scope (Phase 0)
* Scrapers or crawler business logic (Phase 1/2).
* AI/LLM api calls and prompt engineering (Phase 3/4).
* Outreach, email execution, or UI dashboards.

---

### 4. Responsibilities
* **Configuration Manager**: Loads environment variables from `.env` using Pydantic Settings and validates system requirements on boot.
* **Logger Manager**: Formats system events to standard stdout in JSON format with correlation IDs.
* **Database Manager**: Coordinates SQLAlchemy engine creation, connection pooling, and lifecycle management.
* **Redis Manager**: Wraps connection pools, queue push/pop primitives, and cache setters/getters.
* **Event Bus**: Dispatches events asynchronously to registered handlers.
* **Workflow Manager**: Executes registered configurations of task transitions.
* **Master Agent**: Central supervisor listening to main queues, registering services, and managing scheduling.

---

### 5. Inputs
* **`.env` Configuration File**: Contains DB URLs, API keys, hostnames, and ports.
* **System Triggers**: Command-line signals, cron triggers, or API start requests.

---

### 6. Outputs
* **Initialized Systems**: Persistent database pools, Redis client sockets, and logger stream bindings.
* **Operational Logs**: JSON structured log lines written to console/file.
* **EBus Handlers**: Active listener threads awaiting messages.

---

### 7. Workflow
The system startup workflow proceeds as follows:

Load `.env` variables via Config Manager
↓
Initialize JSON Logger
↓
Establish PostgreSQL Connection Pool
↓
Establish Redis Connection Pool
↓
Initialize Event Bus & Register Core Events
↓
Start Agent Registry & Master Agent Skeleton
↓
Begin Health Monitor Polling

---

### 8. Execution Flow
1. **Bootstrap**: `main.py` invokes `ConfigManager.get_settings()`.
2. **Environment Validation**:
   * If validation fails: Raise `ConfigurationError` and terminate boot.
   * If validation passes: Inject configurations into DB, Redis, and Logger modules.
3. **Logger Setup**: Binds standard handlers to capture and format logs.
4. **PostgreSQL Setup**: Initializes SQLAlchemy `async_engine` and verifies connection.
5. **Redis Setup**: Starts Redis connection pool and checks ping responsiveness.
6. **Registry Boot**: Registers available core engines (Search, Audit, etc.) in `AgentRegistry`.
7. **Orchestration**: Start the Event Bus thread to consume background payloads.

---

### 9. Architecture
This module implements the **Infrastructure Layer** and base **Entities/UseCases** of Clean Architecture.
* **Dependency Injection**: Database and Redis managers are injected into downstream services using constructor injection.
* **Interface First**: Define clean abstract classes (`IQueueManager`, `IEventBus`, `IDatabase`) to shield implementations from caller code.
* **High Cohesion**: Every utility module (like `logger.py` or `redis_manager.py`) is dedicated strictly to its single infrastructure purpose.

---

### 10. Components
#### 10.1 Directory Layout
```
/config
  ├── __init__.py
  └── config.py
/core
  ├── __init__.py
  ├── logger.py
  ├── master_agent.py
  ├── agent_registry.py
  ├── scheduler.py
  ├── health_monitor.py
  └── backup_manager.py
/database
  ├── __init__.py
  ├── database.py
  └── redis_manager.py
/events
  ├── __init__.py
  └── event_bus.py
/workflows
  ├── __init__.py
  └── workflow_manager.py
/dashboard
  ├── __init__.py
  └── dashboard.py
/logs
/backups
/tests
  ├── __init__.py
  └── test_foundation.py
```

---

### 11. Interfaces
```python
class IDatabaseManager(ABC):
    @abstractmethod
    async def connect(self) -> None: pass
    @abstractmethod
    async def disconnect(self) -> None: pass
    @abstractmethod
    def get_session(self) -> AsyncSession: pass

class IRedisManager(ABC):
    @abstractmethod
    async def ping(self) -> bool: pass
    @abstractmethod
    async def push_to_queue(self, queue_name: str, payload: str) -> None: pass
    @abstractmethod
    async def pop_from_queue(self, queue_name: str) -> Optional[str]: pass

class IEventBus(ABC):
    @abstractmethod
    def publish(self, event_type: str, data: dict) -> None: pass
    @abstractmethod
    def subscribe(self, event_type: str, handler: Callable) -> None: pass
```

---

### 12. Validation Rules
* **Strict Config Typing**: Settings variables must use strict type definitions (e.g., `PostgresDsn`, `RedisDsn`, `int`, `bool`).
* **Connection Validation**: Database and Redis connections must be ping-verified prior to reporting startup completion.
* **Log Structure Integrity**: Every log payload must contain a minimum set of fields: `timestamp`, `level`, `message`, `correlation_id`.

---

### 13. Failure Handling
* **Database Recovery Protocol**: In case of database connection loss, implement exponential backoff reconnection logic (3 retries at 2s, 4s, 8s). If connection is not restored within 15 seconds, raise a critical alert and transition to FAIL status.
* **Redis Recovery Protocol**: Fall back to in-memory queueing when Redis is unavailable, while outputting CRITICAL warning logs.
* **Exception Shielding**: Wrap system main loop in top-level try/except blocks to log unhandled crashes without exiting execution thread.

---

### 14. Constraints
* Python 3.11+ async constructs must be used (`asyncio`, `async/await`).
* Must use Pydantic V2 for config structure.
* SQL connections must be non-blocking using `asyncpg` driver.
* Absolutely no mock modules allowed in active production profile.

---

### 15. Performance Requirements
* **Startup Latency**: The system must fully initialize and check all infrastructure connections in less than 2.0 seconds.
* **DB Connection Pool Acquisition**: Connection requests from pool must execute in under 10ms.
* **Logging Overhead**: JSON serialization must not add more than 1ms latency to transaction pipelines.

---

### 16. Security Rules
* **No Plain-text Credentials**: All credentials must be extracted from environment variables.
* **Parameter Binding**: No raw SQL string generation. All SQL operations must use parameterized ORM statements.
* **Access Control**: Database connection URI must limit permissions to table read/write scopes.

---

### 17. Logging Requirements
* Logs must write to stdout and to `logs/foundation.log`.
* Log schema:
  ```json
  {
    "timestamp": "2026-07-05T13:00:00.000Z",
    "level": "INFO",
    "correlation_id": "uuid-v4-string",
    "module": "database",
    "message": "Database connection pool established successfully."
  }
  ```

---

### 18. Configuration
```env
# .env Configuration Schema
ENVIRONMENT=development
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/website_agency
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
TELEGRAM_BOT_TOKEN=dummy_token
TELEGRAM_CHAT_ID=dummy_chat
GEMINI_API_KEY=dummy_gemini_key
```

---

### 19. Testing Requirements
* Unit test coverage must exceed 90% for foundation helper scripts.
* Enforce testing using `pytest` and `pytest-asyncio`.
* Integration tests must execute dockerized DB and Redis checks using temporary test containers or local test ports.

---

### 20. Audit Requirements
* Track system boot and shutdown cycles.
* Record duration of system connection sequences.
* Keep persistent tracking logs of active configuration options (hiding secret variables).

---

### 21. PASS Conditions
* System boot finishes with zero exceptions in logs.
* Database connection check passes.
* Redis connection check passes.
* All base directory structures exist.
* `pytest` returns 100% success on foundational tests.

---

### 22. FAIL Conditions
* Database validation timeout.
* Missing mandatory `.env` variable values.
* Port resource locks (e.g., Redis socket occupied or inaccessible).

---

### 23. LOCK Conditions
* Once APPROVED by the client, SDD-001 is locked.
* Downstream modules must strictly use the interfaces and layout specified herein.

---

### 24. Summary
Phase 0 establishes the bedrock foundation of the AI Website Upgrade Agency. It sets up configuration, logging, database connections, and background pub-sub queues. Once validated, this phase unlocks the development of prospecting engines.

---

### 25. Next Document
* **SDD-002**: Search Engine & Website Scraper Design Specification.

---

### DOCUMENT STATUS
* **Current Status**: APPROVED
* **Next Document**: SDD-002

### END OF DOCUMENT
