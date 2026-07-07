# System Design Document (SDD-011)
## Phase 8.6 and 8.7 - Personalization & Prompt Construction Layers

This document outlines the design specifications, selection rules, components, and validation parameters for the Personalization Layer (8.6) and Prompt Construction Layer (8.7).

---

### 1. Personalization Layer (Phase 8.6)
The Personalization Layer consumes the `UnifiedBusinessContext` and extracts targeting tokens for the sales outreach hook:
* **Nomenclature & Wording Rules**:
  - Capitalizes the primary company name (parsed from target domain).
  - Selects modernization hooks based on audit performance scores:
    * If `mobile_score` < 70: Choose `mobile responsiveness optimization` and `mobile viewport adapter`.
    * If `speed_score` < 60: Choose `page speed performance caching` and `optimized load distribution`.
    * Else: Choose `visual design system modernization` and `glassmorphic presentation layers`.
* **Traceability Constraint**:
  - Every selected personalization parameter maps directly back to the audited lead profile attributes.

---

### 2. Prompt Construction Layer (Phase 8.7)
The Prompt Construction Layer compiles the personalization variables and constraints into a standardized, deterministic AI Prompt Package.

#### 2.1 Prompt Structure Ordering
The constructed prompt follows a strict structured template containing:
1. **System Instructions**: Defines the execution behavior for AI generation (e.g. professional agency sales outreach).
2. **Enterprise Writing Rules**: Enforces professional tone, no hype words, clear value statements.
3. **Context Variables**:
   - `Business Context`: Company name, target niche.
   - `Recipient Context`: Contact name, target email.
   - `Website & Audit Context`: Audited domain name, scores.
   - `Prototype Context`: Validated Prototype Redesign preview URL.
4. **Output Requirements**: Subject line and body draft parameters.
5. **Generation Constraints**: Restricts fabricated stats, unverified technical claims, or pushy sales pitches.
