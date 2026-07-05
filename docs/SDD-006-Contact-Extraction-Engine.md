# Software Design Document: SDD-006
## Phase 5 - Contact Extraction Engine Specification

### Status: PENDING APPROVAL

---

## 1. Purpose
Contact Extraction Engine ka main purpose Website Audit Engine aur Niche Detection Engine ke baad target business websites se multi-page crawling ke through active communication channels extract karna hai. Yeh phase fully deterministic, non-AI (rules & regex-based) engineering framework standard follow karega.

---

## 2. Objectives
* Target site aur uske subpages (`/`, `about`, `contact`, `contact-us`, `team`, `support`, `footer`, `privacy`, `terms`) ko efficiently parse karna.
* Social media profiles (Facebook, Instagram, LinkedIn, Twitter/X, YouTube, WhatsApp, Google Business), phone numbers, aur emails extract karna.
* Regex matching se lead info fetch karke standard format me normalise aur validate karna.
* Database record mapping maintain karna (lead status ko update karna: success par `EXTRACTED`, failure par `NO_CONTACT`).
* Downstream validation operations ke liye Redis target `validation_queue` me push karna.

---

## 3. Architecture Overview
Contact Extraction Engine is flow par work karta hai:

```
           [ Lead Scored Event / URL in contact_queue ]
                                 ↓
                        [ ContactAgent ]
                                 ↓
            [ Crawl: Home page using UrllibBrowserEngine ]
                                 ↓
            [ ContactParser: Find internal links (about, contact, etc.) ]
                                 ↓
            [ Crawl subpages & Extract raw links and text ]
                                 ↓
         [ EmailExtractor ]   [ PhoneExtractor ]   [ SocialExtractor ]
                                 ↓
                 [ ContactNormalizer & Validator ]
                                 ↓
                [ DB: Create/Update contacts table ]
                [ DB: Update search_leads status ]
                     (EXTRACTED or NO_CONTACT)
                                 ↓
               [ Redis: push to validation_queue ]
                                 ↓
             [ EventBus: publish contact_extracted ]
```

---

## 4. Database Schema
Nayi table `contacts` create ki jayegi:

### Table: `contacts`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `lead_id` | `Integer` | ForeignKey(`search_leads.id`, ondelete="CASCADE"), Unique, Index | Parent Lead reference |
| `primary_email` | `String(255)` | Nullable=True | Main verified business email |
| `secondary_email` | `String(255)` | Nullable=True | Backup business email |
| `phone` | `String(50)` | Nullable=True | Main phone number |
| `whatsapp` | `String(50)` | Nullable=True | WhatsApp phone or api link |
| `facebook` | `String(255)` | Nullable=True | Facebook profile URL |
| `instagram` | `String(255)` | Nullable=True | Instagram profile URL |
| `linkedin` | `String(255)` | Nullable=True | LinkedIn profile/company URL |
| `twitter` | `String(255)` | Nullable=True | Twitter/X profile URL |
| `youtube` | `String(255)` | Nullable=True | YouTube channel URL |
| `website` | `String(255)` | Nullable=True | Source domain/url website |
| `status` | `String(50)` | Nullable=False | Contact Quality: Complete, Partial, Email Only, Phone Only, Social Only, No Contact |
| `created_at` | `DateTime` | Nullable=False | Creation timestamp (UTC) |
| `updated_at` | `DateTime` | Nullable=False | Modification timestamp (UTC) |

---

## 5. Multi-Page Crawling & Extraction Logic
Crawler performance aur depth limitations ke criteria:
* **Scope Limits**: Home page crawl karne ke baad, anchor elements (`<a>` tags) parse honge. Jo relative paths ya same domain URLs targets `/about`, `/contact`, `/contact-us`, `/team`, `/support`, `/footer`, `/privacy`, `/terms` se partial matching karenge, unhe collection array me add kiya jayega.
* **Domain Lock**: Kisi bhi external link ko crawl nahi kiya jayega.
* **Performance Limits**: Overall site processing timeout standard **10 seconds** se lower rakha jayega (Home page + subpages async concurrency runtime limit).

### 5.1 Extraction Patterns (Regex & Rules):
* **Email Extraction**:
  * Mailto link: `href="mailto:([^"]+)"`
  * Regex search on raw text: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
* **Phone Extraction**:
  * Tel link: `href="tel:([^"]+)"`
  * General regex search: `(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}` (normalised to strip whitespaces and non-numeric chars).
* **Social Links Detection**:
  * Matching anchor domains:
    * Facebook: `facebook.com` or `fb.com`
    * Instagram: `instagram.com`
    * LinkedIn: `linkedin.com`
    * Twitter/X: `twitter.com` or `x.com`
    * YouTube: `youtube.com` or `youtu.be`
    * WhatsApp: `wa.me` or `api.whatsapp.com`
    * Google Business: `google.com/maps`, `g.page`, `maps.google.com`

---

## 6. Normalisation & Validation
* **Email Normalisation**: Lowercase format conversion, leading/trailing whitespace strip.
* **Phone Normalisation**: Digits and optional leading `+` char extraction only. Length bounds (7 to 15 chars).
* **Social Link Normalisation**: Ensure standard protocol scheme `https://` is prepended and trailing slashes are removed.
* **Validator Output Quality Score rules**:
  * **Complete**: Email, Phone, aur kam se kam 1 Social link present ho.
  * **Partial**: Multi-type info present ho par saare required categories nahi (e.g. Email + Phone, Email + Social).
  * **Email Only**: Sirf Email data extracted.
  * **Phone Only**: Sirf Phone data extracted.
  * **Social Only**: Sirf Social profiles data extracted.
  * **No Contact**: Ek bhi communication channel na mile.

---

## 7. Failure Handling & Recovery
* **Unreachable Website**: Agar HTTP connection timed out or socket error throw hota hai, to status value `NO_CONTACT` updated hogi database table state me aur pipeline crashes block honge.
* **External API Integration Block**: Fully deterministic local code. Koy bhi model api (Gemini/OpenAI) use nahi ki jayegi.

---

## 8. State Transitions & Downstream target
* **Transition Succeeded**: Status flow ko change karega from `SCORED` to `EXTRACTED` table state records par.
* **Transition Failed**: Leads target details status updated to `NO_CONTACT` aur validation logic pipeline skipped.
* **Target Queue**: Successfully extracted targets ko downstream Redis `validation_queue` me push kiya jayega.
