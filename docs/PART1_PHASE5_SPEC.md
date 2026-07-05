
<!-- Page 38 -->
​Rules Applied​
​Scores Generated​
​Execution Time​
​PASS / FAIL​
​=================================================================​
​LOCK CONDITION​
​=================================================================​
​Lead Scoring Engine becomes READ ONLY.​
​No future modification allowed unless architecture changes.​
​#################################################################​
​PHASE 5​
​CONTACT EXTRACTION ENGINE​
​#################################################################​
​PURPOSE​
​Extract every possible contact method from a business website.​
​The engine must discover every publicly available communication channel.​
​=================================================================​
​INPUT​
​=================================================================​
​Website URL​
​Audit Report​
​Business Profile​
​=================================================================​
​OUTPUT​
​=================================================================​
​Validated Contact Record​
​=================================================================​

<!-- Page 39 -->
​PAGES TO SCAN​
​=================================================================​
​/​
​about​
​contact​
​contact-us​
​team​
​support​
​footer​
​privacy​
​terms​
​=================================================================​
​CONTACT TYPES​
​=================================================================​
​Primary Email​
​Secondary Email​
​Phone Number​
​WhatsApp​
​Facebook​
​Instagram​
​LinkedIn​
​Twitter​
​YouTube​
​Google Business​

<!-- Page 40 -->
​=================================================================​
​EXTRACTION RULES​
​=================================================================​
​Extract only publicly available information.​
​Never bypass authentication.​
​Never scrape restricted areas.​
​Respect robots.txt where applicable.​
​Store normalized values.​
​Remove duplicates.​
​=================================================================​
​VALIDATION​
​=================================================================​
​Email Format​
​Phone Format​
​Country Code​
​Social URL Validation​
​Duplicate Detection​
​=================================================================​
​FILES TO CREATE​
​=================================================================​
​agents/contact/​
​contact_agent.py​
​contact_parser.py​
​email_extractor.py​
​phone_extractor.py​

<!-- Page 41 -->
​social_extractor.py​
​normalizer.py​
​validator.py​
​tests/​
​=================================================================​
​DATABASE​
​=================================================================​
​contacts​
​Fields​
​id​
​lead_id​
​primary_email​
​secondary_email​
​phone​
​whatsapp​
​facebook​
​instagram​
​linkedin​
​twitter​
​youtube​
​website​
​status​
​=================================================================​

<!-- Page 42 -->
​CONTACT QUALITY​
​=================================================================​
​Complete​
​Partial​
​Email Only​
​Phone Only​
​Social Only​
​No Contact​
​=================================================================​
​PASS CONDITIONS​
​=================================================================​
​Contact Record created.​
​Database updated.​
​Normalization completed.​
​Validation completed.​
​All tests passed.​
​=================================================================​
​FAIL CONDITIONS​
​=================================================================​
​Website unavailable​
​No contact information​
​Parser failure​
​Database failure​
​=================================================================​
​AUDIT REPORT​
​=================================================================​

<!-- Page 43 -->
​Pages Scanned​
​Contacts Found​
​Duplicates Removed​
​Validation Result​
​Execution Time​
​PASS / FAIL​
​=================================================================​
​GLOBAL DEVELOPMENT RULES​
​=================================================================​
​Do NOT continue to Phase 6.​
​Do NOT generate Emails.​
​Do NOT generate HTML Prototypes.​
​Do NOT access Gemini.​
​Do NOT perform AI analysis.​
​These phases must remain completely deterministic.​
​=================================================================​
​QUALITY REQUIREMENTS​
​=================================================================​
​Every class must have a single responsibility.​
​Every service must be independently testable.​
​Business rules must never be hardcoded.​
​Configuration must be external.​
​Logging must exist for every execution step.​
​Every exception must be handled.​

<!-- Page 44 -->
​Every database transaction must be safe.​
​Every function must include documentation.​
​=================================================================​
​TEST COVERAGE​
​=================================================================​
​Minimum Unit Test Coverage​
​90%​
​Integration Tests​
​Required​
​Failure Tests​
​Required​
​Performance Tests​
​Required​
​Regression Tests​
​Required​
​=================================================================​
​END OF PART 2B-2A​
​# AI WEBSITE UPGRADE AGENCY​
​## ENTERPRISE DEVELOPMENT KIT (EDK)​
​### MASTER SYSTEM PROMPT​
​### PART 2B-2B​
​### PHASE 6​
​### EMAIL VALIDATION ENGINE​
​=================================================================​
​MISSION​
​=================================================================​
​Implement only Phase 6.​

<!-- Page 45 -->
​Build a production-grade Email Validation Engine.​
​Do NOT generate emails.​
​Do NOT contact businesses.​
​Do NOT generate HTML prototypes.​
​Do NOT call any AI models.​
​The Email Validation Engine is responsible only for validating, scoring,​
​and classifying email addresses extracted from websites.​
​It must be deterministic, scalable, fast, and inexpensive.​
​=================================================================​
​OBJECTIVE​
​=================================================================​
​Before any outreach campaign begins, every extracted email address must be​
​validated to reduce bounce rate, improve sender reputation, and maximize​
​deliverability.​
​The engine must classify every email into quality levels.​
​Only high-quality emails may proceed to the Email Engine.​
​=================================================================​
​INPUT​
​=================================================================​
​Contact Record​
​Primary Email​
​Secondary Email​
​Website Domain​
​Business Profile​
​=================================================================​
​OUTPUT​
​=================================================================​

<!-- Page 46 -->
​Validated Email Record​
​Email Quality Score​
​Deliverability Status​
​Recommendation​
​=================================================================​
​VALIDATION PIPELINE​
​=================================================================​
​Stage 1​
​Syntax Validation​
​↓​
​Stage 2​
​Domain Validation​
​↓​
​Stage 3​
​DNS Lookup​
​↓​
​Stage 4​
​MX Record Verification​
​↓​
​Stage 5​
​Disposable Email Detection​
​↓​
​Stage 6​

<!-- Page 47 -->
​Role-based Email Detection​
​↓​
​Stage 7​
​Catch-all Domain Detection​
​↓​
​Stage 8​
​Business Domain Matching​
​↓​
​Stage 9​
​Confidence Score​
​↓​
​Final Classification​
​=================================================================​
​SYNTAX VALIDATION​
​=================================================================​
​Validate according to RFC standards.​
​Reject:​
​Missing @​
​Missing domain​
​Invalid characters​
​Invalid TLD​
​Multiple @ symbols​
​Whitespace​

<!-- Page 48 -->
​Malformed addresses​
​=================================================================​
​DOMAIN VALIDATION​
​=================================================================​
​Verify:​
​Domain exists​
​Domain resolves​
​Domain not expired (when possible)​
​No invalid hostname​
​=================================================================​
​MX RECORD VALIDATION​
​=================================================================​
​Verify​
​MX Records​
​SMTP Availability (optional)​
​Mail Server Presence​
​DNS Health​
​=================================================================​
​DISPOSABLE EMAIL DETECTION​
​=================================================================​
​Reject common temporary providers.​
​Examples​
​10MinuteMail​
​Guerrilla Mail​
​Mailinator​

<!-- Page 49 -->
​TempMail​
​Disposable providers must receive​
​Quality Score = 0​
​=================================================================​
​ROLE BASED EMAILS​
​=================================================================​
​Detect​
​info@​
​support@​
​sales@​
​contact@​
​admin@​
​office@​
​hello@​
​careers@​
​Role-based emails are valid.​
​However,​
​assign lower personalization score.​
​=================================================================​
​BUSINESS DOMAIN MATCHING​
​=================================================================​
​Compare​
​Website Domain​
​↓​

<!-- Page 50 -->
​Email Domain​
​Example​
​Website​
​company.com​
​Email​
​hello@company.com​
​Result​
​Perfect Match​
​-----------------------------------------​
​Website​
​company.com​
​Email​
​gmail.com​
​Result​
​Generic Email​
​Lower Confidence​
​=================================================================​
​EMAIL QUALITY SCORE​
​=================================================================​
​100​
​Perfect​
​90​
​Business Email​

<!-- Page 51 -->
​80​
​Verified Generic​
​60​
​Role Email​
​30​
​Questionable​
​0​
​Invalid​
​=================================================================​
​CLASSIFICATION​
​=================================================================​
​Premium​
​Business Verified​
​Verified​
​Generic​
​Role-based​
​Temporary​
​Invalid​
​Rejected​
​=================================================================​
​DATABASE​
​=================================================================​
​Table​
​validated_emails​

<!-- Page 52 -->
​Fields​
​id​
​lead_id​
​email​
​quality_score​
​classification​
​mx_status​
​domain_status​
​disposable​
​role_based​
​confidence​
​recommended_action​
​validated_at​
​=================================================================​
​FILES TO CREATE​
​=================================================================​
​agents/email_validation/​
​email_validation_agent.py​
​syntax_validator.py​
​dns_validator.py​
​mx_validator.py​
​disposable_detector.py​
​role_detector.py​

<!-- Page 53 -->
​confidence_engine.py​
​quality_score.py​
​validation_models.py​
​tests/​
​=================================================================​
​CONFIGURATION​
​=================================================================​
​Validation Threshold​
​Minimum Quality Score​
​Allowed Domains​
​Blocked Domains​
​Disposable Database​
​Timeout Values​
​Retry Count​
​=================================================================​
​LOGGING​
​=================================================================​
​Every validation step must log​
​Validation Start​
​Validation Success​
​Validation Failure​
​DNS Result​
​MX Result​
​Confidence Score​

<!-- Page 54 -->
​Execution Time​
​=================================================================​
​ERROR HANDLING​
​=================================================================​
​Handle​
​DNS Timeout​
​Network Failure​
​Invalid Email​
​Unknown MX​
​Malformed Domain​
​Retry Logic​
​Graceful Failure​
​=================================================================​
​PERFORMANCE REQUIREMENTS​
​=================================================================​
​Average Validation Time​
​< 2 seconds​
​Parallel Validation​
​Supported​
​Caching​
​Required​
​DNS Cache​
​Recommended​
​=================================================================​
