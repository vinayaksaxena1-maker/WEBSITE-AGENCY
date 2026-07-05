# Software Design Document: SDD-004
## Phase 3 - Niche Detection Engine Specification

### Status: PENDING APPROVAL

---

## 1. Purpose
Niche Detection Engine ka purpose leads (websites) ke page content aur audit data ko analyze karke unke actual business category (niche) ko automatically classify karna hai, taaki downstream engines unhe custom web templates aur personalized emails offer kar sakein.

---

## 2. Objectives
* Web HTML pages aur text signals se business niche auto-detect karna.
* High classification accuracy ($\ge 90\%$) achieve karna.
* **Hybrid Classification Pattern** implement karna: Pehle locally pattern-matching Rule Engine chalega (zero latency & cost), aur agar confidence kam ho toh Gemini AI fallback trigger hoga.
* Niche ke specifications ke according custom web design themes recommend karna.
* Profiles ko `business_profiles` table me persist karna aur events dispatch karna.

---

## 3. Architecture Overview
Niche Detection Engine ko hum decoupled, hybrid model me structure karenge:

```
                  [ Audit Completed / Lead URL ]
                                ↓
                        [ NicheAgent ]
                                ↓
                      [ NicheClassifier ]
                       /              \
         (Confidence >= 0.85)    (Confidence < 0.85)
                   /                      \
        [ RuleEngine (Local) ]     [ Gemini AI Fallback ]
                   \                      /
                    \                    /
                      [ ThemeMapper ]
                                ↓
                  [ DB: business_profiles ]
                                ↓
                    [ Redis: scoring_queue ]
```

---

## 4. Database Schema
Nayi table `business_profiles` SQLite aur PostgreSQL dono ke liye niche likhi specifications ke according banayi jayegi:

### Table: `business_profiles`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `lead_id` | `Integer` | ForeignKey(`search_leads.id`), Unique, Index | Parent Lead reference |
| `industry` | `String(50)` | Nullable=False | Mapped business category (e.g. "Hospital") |
| `confidence` | `Float` | Nullable=False | Mapped confidence level (0.0 to 1.0) |
| `recommended_theme` | `String(100)` | Nullable=False | Suggested design layout identifier |
| `schema_version` | `String(10)` | Nullable=False (Default: "1.0.0") | Database schema model version |
| `classifier_version` | `String(10)` | Nullable=False (Default: "1.0.0") | Rules/AI classification logic version |
| `created_at` | `DateTime` | Nullable=False | Timestamp of creation (UTC aware) |
| `updated_at` | `DateTime` | Nullable=False | Timestamp of modification (UTC aware) |

---

## 5. Supported Categories
Niche Detection Engine niche likhi classes me se kisi ek me leads ko classify karega:
* `Publisher`
* `School`
* `Hospital`
* `Clinic`
* `Restaurant`
* `Hotel`
* `Travel`
* `Law Firm`
* `Real Estate`
* `NGO`
* `Gym`
* `Education`
* `Portfolio`
* `Business`
* `Corporate`

---

## 6. Hybrid Classification Logic (Rule Engine + AI)

### Step A: Local Rule Engine (Keyword Pattern Matching)
Pehle local matching run hogi. Hum HTML title, description, headers (`h1`, `h2`), aur visible text me niche keywords scan karenge:
* **Hospital / Clinic**: keywords = `["hospital", "clinic", "medical", "doctor", "health", "care", "patient", "treatment", "physician"]`
* **Gym**: keywords = `["gym", "fitness", "workout", "crossfit", "train", "bodybuilding", "yoga", "coaching"]`
* **Law Firm**: keywords = `["lawyer", "attorney", "law firm", "advocate", "legal", "counsel", "solicitor", "justice"]`
* **School / Education**: keywords = `["school", "academy", "college", "university", "education", "course", "degree", "student"]`
* **Restaurant / Hotel**: keywords = `["restaurant", "food", "cafe", "dining", "menu", "hotel", "resort", "suite", "stay"]`

*Confidence Score Calculation*:
$$\text{Confidence} = \frac{\text{Matching Keywords Count}}{\text{Category Factor}}$$
* If `Confidence >= 0.85`, hum local match ko final karenge (No AI call).

### Step B: AI Fallback (Gemini API Integration)
* **Trigger Condition**: Agar Rule Engine ka maximum confidence score $< 0.85$ ho ya category match "Unknown" ho.
* **Context Payload**: AI prompt me title, metadata, aur main text snippet share kiya jayega.
* **Structured Output Schema**:
  ```json
  {
    "industry": "Hospital",
    "confidence": 0.95
  }
  ```

---

## 7. Theme Mapping Table
Niche classification ke according Theme Engine niche likhe modern templates recommend karega:

| Classified Industry | Recommended Theme |
| :--- | :--- |
| `Hospital` / `Clinic` | `clinical_comfort` |
| `School` / `Education` | `academic_prestige` |
| `Gym` | `energy_dynamic` |
| `Restaurant` / `Hotel` | `luxury_hospitality` |
| `Law Firm` | `justice_executive` |
| `Real Estate` | `urban_estate` |
| `NGO` | `impact_trust` |
| `Publisher` / `Corporate` / `Business` | `corporate_edge` |
| `Portfolio` | `creative_showcase` |
| `Travel` | `wanderlust_adventure` |

---

## 8. Failure Handling & Retry Strategy
* **Gemini Timeout / Network failure**: Agar API call block hoti hai, toh execution crash nahi hoga. It will fallback to standard default category (`Business`, confidence: `0.50`, theme: `corporate_edge`) aur log raise karega.
* **Database Deadlock**: Session commit ko transaction managers ke automatic retry (maximum 3 times) loop me wrap kiya jayega.

---

## 9. PASS & FAIL Conditions

### PASS Conditions
* Website niche successfully detect and classify ho rahi hai.
* Rule engine fallback validation successful hai.
* Database updates atomic transactions me perform ho rahe hain (business profiles update + lead status `CLASSIFIED`).
* Unit tests successfully pass ho rahe hain ($\ge 90\%$ test coverage).

### FAIL Conditions
* AI connection drop hone par system ka crash ho jana (Unhandled Exceptions).
* Duplicate insertions or primary key unique constraint crash on `business_profiles`.
* Leads ka status update fail hona.
