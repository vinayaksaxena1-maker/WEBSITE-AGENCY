# Software Design Document: SDD-005
## Phase 4 - Lead Scoring Engine Specification

### Status: PENDING APPROVAL

---

## 1. Purpose
Lead Scoring Engine ka main purpose Website Audit Engine aur Niche Detection Engine ke outputs ko process karke lead quality and upgrade priority metrics generate karna hai. Yeh engine aage ke downstream workflows ke liye cost-optimization filter ki tarah kaam karta hai (Gemini API prototype and email operations expensive hain, isliye unhe sirf high-priority leads par chalaya jayega).

---

## 2. Objectives
* Web page checks (SSL, speed, responsive, content) ke scores ke baseline par upgrade potential calculate karna.
* EDK-compliant 0-100 base score rules compile karna.
* Multi-dimensional formula use karke **Business Value Index (BVI)** compute karna.
* Leads ko prioritised levels (`Low Priority`, `Medium Priority`, `High Priority`, `Premium Lead`) me classify karna.
* Decisions ko `lead_scores` table me persist karna, status update karna, aur downstream event trigger karna.

---

## 3. Architecture Overview
Lead Scoring Engine is flow par work karta hai:

```
           [ Niche Detected Event / URL in scoring_queue ]
                                 ↓
                        [ ScoringAgent ]
                                 ↓
            [ Read: audits & business_profiles tables ]
                                 ↓
         [ ScoringCalculator ]       [ BusinessValueCalculator ]
           (Calculate Score)           (Calculate BVI & priority)
                                 \   /
                                  \ /
                                   ↓
                       [ DB: lead_scores table ]
                       [ DB: Update status to SCORED ]
                                   ↓
                   [ Redis: push to contact_queue ]
                                   ↓
                 [ EventBus: publish lead_scored ]
```

---

## 4. Database Schema
Nayi table `lead_scores` downstream validation pipelines ke reference ke liye create ki jayegi:

### Table: `lead_scores`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `lead_id` | `Integer` | ForeignKey(`search_leads.id`), Unique, Index | Parent Lead reference |
| `lead_score` | `Integer` | Nullable=False | Calculated upgrade score (0 to 100) |
| `priority_level` | `String(50)` | Nullable=False | Mapped priority stage name |
| `business_value_index` | `Float` | Nullable=False | Calculated Value Index (0.0 to 2.0+) |
| `ai_processing_decision` | `String(50)` | Nullable=False | Proceed, Ignore, Manual Review, or Immediate Processing |
| `improvement_opportunities` | `Text` | Nullable=True | Comma-separated list of identified website issues |
| `schema_version` | `String(10)` | Nullable=False (Default: "1.0.0") | Database schema version |
| `rules_version` | `String(10)` | Nullable=False (Default: "1.0.0") | Rules engine scoring version |
| `created_at` | `DateTime` | Nullable=False | Creation timestamp (UTC) |
| `updated_at` | `DateTime` | Nullable=False | Modification timestamp (UTC) |

---

## 5. Scoring Metrics & Weights
Audit metrics par base points evaluate kiye jayenge, total max lead score limit **100** hai:

* **Old Website Design (+30)**: `design_score` < 50
* **Mobile Responsiveness Issues (+25)**: `mobile_score` < 70
* **Performance Problems (+20)**: `speed_score` < 60
* **SEO Problems (+15)**: `seo_score` < 70
* **Trust Issues (+10)**: `trust_score` < 70
* **Broken Navigation (+10)**: `seo_score` < 50 OR `design_score` < 40
* **Poor CTA Placement (+10)**: `design_score` < 60 OR `cta_buttons_detected` is False
* **Outdated Branding (+15)**: `design_score` < 50
* **No SSL (+10)**: Audit summary contains "SSL invalid/missing"
* **Accessibility Problems (+10)**: `mobile_score` < 80 OR `design_score` < 80

---

## 6. Business Value Score & Index Formulas
Business Value Index (BVI) calculate karne ke liye niche likhi equation ka use kiya jayega:

$$\text{BVI} = \text{Website Deficiencies} \times \text{Niche Confidence} \times \text{Industry Multiplier} \times \text{Contact Multiplier} \times \text{Lead Score Factor}$$

### Factors Mapping:
1. **Website Deficiencies**:
   $$\text{Deficiencies} = \frac{100 - \text{audit.audit\_score}}{100.0}$$
2. **Niche Confidence**:
   $$\text{Confidence} = \text{business\_profile.confidence}$$
3. **Industry Multiplier**:
   * `1.5`: `Real Estate`, `Law Firm`, `Hospital`, `Clinic`, `Hotel`
   * `1.2`: `Restaurant`, `Gym`, `Travel`, `Business`, `Corporate`
   * `1.0`: `School`, `Education`, `NGO`
   * `0.8`: `Publisher`, `Portfolio`
   * `1.0` (Default fallback for other niches)
4. **Contact Multiplier**:
   * `1.2` if `audit.trust_score >= 50` (shows presence of contact page / tel link).
   * `0.8` if `audit.trust_score < 50`.
5. **Lead Score Factor**:
   $$\text{Lead Score Factor} = \frac{\text{lead\_score}}{100.0}$$

---

## 7. Priority Levels & AI Processing Decision
Calculated Lead Score ke points range ke criteria par outputs set honge:

| Lead Score Range | Priority Level | AI Processing Decision | Recommended Actions |
| :--- | :--- | :--- | :--- |
| `0 - 30` | `Low Priority` | `IGNORE` | Target process skip. No AI prototype generated. |
| `31 - 60` | `Medium Priority` | `MANUAL_REVIEW` | Manual inspection required before starting prototype. |
| `61 - 80` | `High Priority` | `PROCEED` | Enqueued downstream for automatic AI prototype. |
| `81 - 100` | `Premium Lead` | `IMMEDIATE_PROCESSING` | Highest priority execution. Highlight premium tier in emails. |

---

## 8. Failure Handling & Recovery
* **Missing Audit / Profile Records**: Agar lead_id ke andhar audit data ya business profile details missing honge, toh scoring agent crash nahi karega. Yeh `IGNORE` level priority calculate karega with defaults (scores: 0, BVI: 0.0) and error log context trace record karega.
* **Downstream Queue failure**: Queue push block hone par execution raise warnings karega par database commit safe rakhega.

---

## 9. PASS & FAIL Conditions

### PASS Conditions
* Target lead score standard weights ke criteria par successfully compute ho raha hai.
* Business Value Index (BVI) calculation complete and correct floating format me numeric output return karta hai.
* Lead table status `SCORED` me correctly change ho rahi hai.
* Unit tests successfully compile and pass ho rahe hain ($\ge 90\%$ test coverage).

### FAIL Conditions
* Division by zero or negative mathematical score values logic block exceptions throw kare.
* Duplicate lead inserts crash SQLite transactions.
* Event publishing errors lead flow verify block karein.
