# Part 3 Specification: Pages 54 to 73


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

<!-- Page 55 -->
​RECOMMENDED ACTIONS​
​=================================================================​
​Premium​
​Proceed Immediately​
​------------------------------------​
​Verified​
​Proceed​
​------------------------------------​
​Role Based​
​Proceed​
​Use Generic Email Template​
​------------------------------------​
​Generic​
​Proceed​
​Lower Priority​
​------------------------------------​
​Temporary​
​Reject​
​------------------------------------​
​Invalid​
​Reject​
​=================================================================​
​TEST CASES​
​=================================================================​

<!-- Page 56 -->
​Valid Business Email​
​Valid Gmail​
​Role Email​
​Temporary Email​
​Invalid Email​
​Missing Domain​
​Broken MX​
​Fake Domain​
​Expired Domain​
​Duplicate Email​
​=================================================================​
​UNIT TESTS​
​=================================================================​
​Syntax​
​DNS​
​MX​
​Classification​
​Quality Score​
​Confidence Engine​
​Caching​
​=================================================================​
​INTEGRATION TESTS​
​=================================================================​
​Database Storage​

<!-- Page 57 -->
​Logging​
​Queue Integration​
​Configuration​
​=================================================================​
​PASS CONDITIONS​
​=================================================================​
​All validations complete successfully.​
​Quality score generated.​
​Classification generated.​
​Database updated.​
​Logs generated.​
​90%+ unit test coverage.​
​Integration tests pass.​
​Performance target achieved.​
​=================================================================​
​FAIL CONDITIONS​
​=================================================================​
​Validation Crash​
​Database Failure​
​Configuration Error​
​Repeated DNS Failure​
​Unhandled Exception​
​=================================================================​
​AUDIT REPORT​
​=================================================================​

<!-- Page 58 -->
​Files Created​
​Validation Rules​
​Execution Time​
​Emails Validated​
​Invalid Emails​
​Role Emails​
​Temporary Emails​
​Database Changes​
​Warnings​
​Errors​
​PASS / FAIL​
​=================================================================​
​LOCK CONDITIONS​
​=================================================================​
​After PASS​
​Phase 6 becomes READ ONLY.​
​No changes are allowed unless architecture approval is granted.​
​=================================================================​
​GLOBAL RESTRICTIONS​
​=================================================================​
​Do NOT generate Emails.​
​Do NOT contact businesses.​
​Do NOT create HTML prototypes.​
​Do NOT access Gemini.​

<!-- Page 59 -->
​Do NOT access OpenAI.​
​Do NOT implement CRM.​
​Do NOT continue to Phase 7.​
​# AI WEBSITE UPGRADE AGENCY​
​## ENTERPRISE DEVELOPMENT KIT (EDK)​
​### MASTER SYSTEM PROMPT​
​### PART 2B-2C​
​### PHASE 7.1​
​### PROTOTYPE INTELLIGENCE ENGINE (PIE)​
​### FOUNDATION & CORE ARCHITECTURE​
​=================================================================​
​MISSION​
​=================================================================​
​Implement only Phase 7.​
​Do not continue to Phase 8.​
​Prototype Intelligence Engine is responsible for producing a professional​
​responsive HTML website prototype based on an existing business website.​
​The generated prototype must demonstrate how the customer's website can be​
​improved.​
​The engine is not intended to clone the original website.​
​It must generate an improved design while preserving the business identity.​
​=================================================================​
​OBJECTIVE​
​=================================================================​
​Generate a high-quality responsive HTML prototype using:​
​• Existing Website​
​• Website Screenshot​
​• DOM Structure​
​• Business Category​
​• Theme Library​
​• Component Library​

<!-- Page 60 -->
​Output must be production-quality preview code.​
​=================================================================​
​PRIMARY GOALS​
​=================================================================​
​Improve Design​
​Improve UX​
​Improve Mobile Experience​
​Improve CTA Placement​
​Improve Visual Hierarchy​
​Improve Trust Signals​
​Improve Branding​
​Improve Readability​
​Improve Conversion Potential​
​=================================================================​
​INPUTS​
​=================================================================​
​Website URL​
​Audit Report​
​Business Profile​
​Lead Information​
​Business Category​
​Theme Recommendation​
​=================================================================​
​OUTPUTS​
​=================================================================​

<!-- Page 61 -->
​Responsive HTML Prototype​
​CSS​
​Tailwind Layout​
​Preview Screenshot​
​Prototype Metadata​
​Generation Report​
​=================================================================​
​ENGINE RESPONSIBILITIES​
​=================================================================​
​The Prototype Intelligence Engine shall:​
​Capture Website​
​Analyze Structure​
​Understand Business Type​
​Select Theme​
​Generate Layout​
​Build Components​
​Apply Responsive Rules​
​Generate HTML​
​Generate Preview​
​Generate Report​
​=================================================================​
​OUT OF SCOPE​
​=================================================================​
​Do not copy copyrighted assets.​

<!-- Page 62 -->
​Do not duplicate website source code.​
​Do not scrape protected resources.​
​Do not reproduce brand identities without transformation.​
​Do not generate production deployment packages.​
​Generate demonstration prototypes only.​
​=================================================================​
​HIGH LEVEL PIPELINE​
​=================================================================​
​Website URL​
​↓​
​Browser Engine​
​↓​
​Screenshot Engine​
​↓​
​DOM Analyzer​
​↓​
​Business Context​
​↓​
​Theme Engine​
​↓​
​Component Engine​
​↓​
​Layout Generator​

<!-- Page 63 -->
​↓​
​Responsive Engine​
​↓​
​HTML Generator​
​↓​
​Preview Generator​
​↓​
​Prototype Report​
​=================================================================​
​CORE MODULES​
​=================================================================​
​Module 1​
​Browser Engine​
​Module 2​
​Screenshot Engine​
​Module 3​
​DOM Intelligence​
​Module 4​
​Visual Intelligence​
​Module 5​
​Theme Intelligence​
​Module 6​
​Layout Intelligence​

<!-- Page 64 -->
​Module 7​
​Component Generator​
​Module 8​
​Responsive Engine​
​Module 9​
​HTML Generator​
​Module 10​
​Preview Generator​
​Module 11​
​Quality Analyzer​
​=================================================================​
​FILES TO CREATE​
​=================================================================​
​agents/prototype/​
​prototype_agent.py​
​browser_engine.py​
​screenshot_engine.py​
​dom_analyzer.py​
​visual_analyzer.py​
​theme_engine.py​
​layout_engine.py​
​component_engine.py​
​responsive_engine.py​

<!-- Page 65 -->
​html_generator.py​
​preview_generator.py​
​quality_analyzer.py​
​prototype_models.py​
​prototype_pipeline.py​
​tests/​
​=================================================================​
​DATABASE​
​=================================================================​
​prototype_jobs​
​prototype_results​
​prototype_assets​
​prototype_reports​
​=================================================================​
​TABLE​
​prototype_jobs​
​=================================================================​
​id​
​lead_id​
​website_url​
​status​
​theme​
​started_at​
​completed_at​

<!-- Page 66 -->
​=================================================================​
​TABLE​
​prototype_results​
​=================================================================​
​id​
​job_id​
​html_path​
​css_path​
​preview_path​
​quality_score​
​generation_time​
​=================================================================​
​TABLE​
​prototype_reports​
​=================================================================​
​id​
​job_id​
​summary​
​improvements​
​warnings​
​recommendations​
​=================================================================​
​CONFIGURATION​
​=================================================================​
​Viewport Width​
​Viewport Height​

<!-- Page 67 -->
​Browser Type​
​Theme Library​
​Component Library​
​Output Directory​
​Screenshot Quality​
​Preview Resolution​
​Retry Count​
​Timeout​
​=================================================================​
​LOGGING​
​=================================================================​
​Log:​
​Job Start​
​Screenshot Start​
​DOM Analysis​
​Theme Selection​
​HTML Generation​
​Preview Generation​
​Export​
​Errors​
​Completion​
​=================================================================​
​ERROR HANDLING​
​=================================================================​

<!-- Page 68 -->
​Website Timeout​
​Screenshot Failure​
​DOM Failure​
​Theme Failure​
​HTML Failure​
​Preview Failure​
​Export Failure​
​All failures must produce structured logs.​
​=================================================================​
​PASS CONDITIONS​
​=================================================================​
​Screenshot Captured​
​DOM Parsed​
​Theme Selected​
​Responsive HTML Generated​
​Preview Generated​
​Database Updated​
​Logs Written​
​Tests Passed​
​=================================================================​
​FAIL CONDITIONS​
​=================================================================​
​Website Unreachable​
​Screenshot Failed​

<!-- Page 69 -->
​DOM Parsing Failed​
​Theme Missing​
​Generation Failed​
​Unhandled Exception​
​=================================================================​
​GLOBAL RESTRICTIONS​
​=================================================================​
​Do NOT implement Email Engine.​
​Do NOT implement CRM.​
​Do NOT implement Telegram.​
​Do NOT continue to Phase 8.​
​Wait for:​
​Phase 7.2​
​Screenshot Intelligence Engine​
​=================================================================​
​# AI WEBSITE UPGRADE AGENCY​
​## ENTERPRISE DEVELOPMENT KIT (EDK)​
​### MASTER SYSTEM PROMPT​
​### PART 2B-2C​
​### PHASE 7.2​
​### SCREENSHOT INTELLIGENCE ENGINE​
​=================================================================​
​MISSION​
​=================================================================​
​Implement only the Screenshot Intelligence Engine.​
​Do NOT implement DOM Intelligence.​
​Do NOT implement Theme Intelligence.​

<!-- Page 70 -->
​Do NOT implement HTML Generation.​
​Do NOT implement Preview Generation.​
​Do NOT continue to Phase 7.3.​
​This module is responsible only for capturing high-quality website​
​screenshots that will be used by every downstream Prototype​
​Intelligence Engine module.​
​This engine becomes the visual data provider for the entire Prototype​
​Generation Pipeline.​
​=================================================================​
​OBJECTIVE​
​=================================================================​
​Capture a complete, accurate and production-quality visual​
​representation of a business website.​
​The Screenshot Engine must support websites of different sizes,​
​technologies and layouts while producing consistent screenshots​
​for AI analysis.​
​=================================================================​
​PRIMARY RESPONSIBILITIES​
​=================================================================​
​Open Website​
​Wait for Stable Page​
​Handle Dynamic Loading​
​Scroll Complete Page​
​Capture Full Page​
​Capture Desktop View​
​Capture Tablet View​
​Capture Mobile View​

<!-- Page 71 -->
​Store Metadata​
​Export Images​
​Log Results​
​=================================================================​
​INPUT​
​=================================================================​
​Website URL​
​Browser Configuration​
​Viewport Configuration​
​Timeout Configuration​
​Output Directory​
​=================================================================​
​OUTPUT​
​=================================================================​
​Desktop Screenshot​
​Tablet Screenshot​
​Mobile Screenshot​
​Full Page Screenshot​
​Screenshot Metadata​
​Execution Report​
​=================================================================​
​ENGINE PIPELINE​
​=================================================================​
​Website URL​
​↓​

<!-- Page 72 -->
​Launch Browser​
​↓​
​Initialize Context​
​↓​
​Configure Viewport​
​↓​
​Navigate​
​↓​
​Wait Until Stable​
​↓​
​Scroll Page​
​↓​
​Lazy Load Detection​
​↓​
​Image Completion​
​↓​
​Animation Freeze​
​↓​
​Capture Desktop​
​↓​
​Capture Tablet​
​↓​

<!-- Page 73 -->
​Capture Mobile​
​↓​
​Capture Full Page​
​↓​
​Compress Images​
​↓​
​Store Files​
​↓​
​Generate Metadata​
​=================================================================​
​SUPPORTED VIEWPORTS​
​=================================================================​
​Desktop​
​1920 × 1080​
​-------------------------------------​
​Laptop​
​1440 × 900​
​-------------------------------------​
​Tablet​
​768 × 1024​
​-------------------------------------​
​Mobile​
​390 × 844​
