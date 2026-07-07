# Software Design Document: SDD-019
## Phase 7.12 - Prototype Export Engine Specification

### Status: PENDING AUDIT

---

## 1. Purpose
Prototype Export Engine ka primary role certified responsive prototypes aur unke associated assets (.css, images, preview screenshots) ko single package standard ZIP format aur static directory structure me bundle karna hai. Subsystem deterministic manifest aur integrity SHA-256 checksums compute karega, bina any external API connectivity.

---

## 2. Static Website Packaging Layout
The export package structures the generated prototype inside the output directory path:

```
prototype_export/
├── index.html
├── manifest.json
├── README.md
├── LICENSE.txt
├── assets/
│   ├── css/
│   │   └── mock_prototype.css
│   ├── js/
│   ├── images/
│   ├── icons/
│   └── fonts/
└── reports/
    ├── quality_audit.md
    └── preview_audit.md
```

---

## 3. Build Manifest & Checksums Template
* **manifest.json**: Details the project and build configuration metadata.
  * Version tracking
  * Number of compiled components
  * Static file hashes (SHA-256 checksums)
* **Checksum generation**: Computes SHA-256 hashing keys of ZIP and static artifacts to guarantee delivery payload integrity.

---

## 4. Database Schema: `prototype_exports`
SQLite dialect conformed schema representation:

### Table: `prototype_exports`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Autoincrement | Record Identifier |
| `job_id` | `Integer` | ForeignKey(`prototype_jobs.id`, ondelete="CASCADE"), Unique, Index | Reference to parent prototype job |
| `export_version` | `String(50)` | Nullable=False, Default='1.0.0' | SemVer export package version |
| `package_name` | `String(200)` | Nullable=False | Name of generated export ZIP file |
| `package_size` | `Integer` | Nullable=False | Size of the ZIP archive package in bytes |
| `checksum` | `String(100)` | Nullable=False | SHA-256 integrity checksum hash key |
| `export_status` | `String(50)` | Nullable=False, Default='COMPLETED' | Status of export build package creation |
| `validation_status` | `String(50)` | Nullable=False, Default='PASSED' | Final verification status of generated assets |
| `generated_at` | `DateTime(timezone=True)` | Nullable=False | Timezone-aware UTC timestamp |
