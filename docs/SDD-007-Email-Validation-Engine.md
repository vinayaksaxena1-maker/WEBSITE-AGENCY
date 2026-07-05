# Software Design Document: SDD-007
## Phase 6 - Email Validation Engine Specification

### Status: PENDING APPROVAL

---

## 1. Purpose
Email Validation Engine ka main purpose Phase 5 (Contact Extraction Engine) se extract kiye gaye email addresses ko outreach campaign se pehle validate, score, aur classify karna hai. Yeh filter bounce rate minimize aur sender domain reputation protect karne ke liye design kiya gaya hai. Yeh engine fully deterministic (non-AI) hai.

---

## 2. Objectives
* Extracted email addresses ke formats standard syntax RFC parameters par check karna.
* Domain resolve hona aur active MX records structure verify karna (DNS verification).
* Disposable (temp) mail services aur role-based (info@, support@) patterns detect karna.
* Validation metrics par base score aur confidence rate calculate karna.
* Lead details ko database `validated_emails` table me persist karna.
* Lead table status transition manage karna (success: `EXTRACTED` $\rightarrow$ `VALIDATED`, failure: `INVALID_EMAIL`).
* Successfully validated leads ko downstream Redis target `prototype_queue` me push karna.

---

## 3. Architecture Overview
Email Validation Engine is flow par work karta hai:

```
          [ Contact Extracted Event / URL in validation_queue ]
                                 ↓
                    [ EmailValidationAgent ]
                                 ↓
             [ Fetch email records from contacts table ]
                                 ↓
                     [ Validation Pipeline ]
              (Syntax → Domain → DNS → MX → Role → Temp)
                                 ↓
                     [ QualityScoreCalculator ]
                                 ↓
                    [ ConfidenceEngine & Action ]
                                 ↓
             [ DB: Create/Update validated_emails table ]
             [ DB: Update search_leads status ]
                     (VALIDATED or INVALID_EMAIL)
                                 ↓
               [ Redis: push to prototype_queue ]
                                 ↓
             [ EventBus: publish email_validated ]
```

---

## 4. Database Schema
Nayi table `validated_emails` create ki jayegi:

### Table: `validated_emails`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `lead_id` | `Integer` | ForeignKey(`search_leads.id`, ondelete="CASCADE"), Unique, Index | Parent Lead reference |
| `email` | `String(255)` | Nullable=False | Validated email address string |
| `quality_score` | `Integer` | Nullable=False | 0 to 100 quality score |
| `classification` | `String(50)` | Nullable=False | Mapped category level |
| `mx_status` | `String(50)` | Nullable=False | MX record check status |
| `domain_status` | `String(50)` | Nullable=False | DNS resolution status |
| `disposable` | `Boolean` | Nullable=False | True if domain is temporary provider |
| `role_based` | `Boolean` | Nullable=False | True if prefix is department role |
| `confidence` | `Float` | Nullable=False | Calculated confidence factor (0.0 to 1.0) |
| `recommended_action` | `String(50)` | Nullable=False | Mapped action (Proceed, Reject, etc.) |
| `validated_at` | `DateTime` | Nullable=False | Verification timestamp (UTC) |

---

## 5. Multi-Stage Validation Pipeline

### 5.1 Syntax Check
* Regex verification for RFC syntax compliance: `^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`.
* Whitespace, missing symbols, and multiple `@` checks.

### 5.2 Domain & DNS Lookup
* Check if hostname has valid format and resolves to IP address via standard lookup.

### 5.3 MX Records Verification
* Query DNS for `MX` records to confirm server receives mail.

### 5.4 Disposable & Role-based Detection
* **Disposable check**: Match domain against temporary list (e.g., `mailinator.com`, `10minutemail.com`, `guerrillamail.com`, `tempmail.com`, etc.).
* **Role check**: Check prefix matching: `info`, `support`, `sales`, `contact`, `admin`, `office`, `hello`, `careers`.

### 5.5 Business Domain Matching
* Check if email domain matches base website domain. E.g., `website.com` matching `hello@website.com` vs generic `gmail.com`.

---

## 6. Email Quality Score & Classification
* **Perfect (100)**: Business Domain matched, valid MX, non-role.
* **Business Verified (90)**: Valid MX, non-role, but slightly different business domain (valid match).
* **Verified Generic (80)**: Valid generic email (e.g., @gmail.com) with active MX.
* **Role Email (60)**: Valid business/generic email but role-based prefix.
* **Questionable (30)**: Valid syntax but no active MX or slow response.
* **Invalid (0)**: Syntax error or disposable email.

### Recommended Actions Mapping:
* `Premium` $\rightarrow$ `Proceed Immediately`
* `Verified` $\rightarrow$ `Proceed`
* `Role Based` $\rightarrow$ `Proceed with Generic Template`
* `Generic` $\rightarrow$ `Proceed with Lower Priority`
* `Temporary` $\rightarrow$ `Reject`
* `Invalid` $\rightarrow$ `Reject`

---

## 7. Performance & Caching
* **Validation Timeout**: Async execution DNS queries should time out under **2 seconds** per check.
* **DNS Caching**: Local caching of query results to prevent DNS server rate-limiting/throttling.
