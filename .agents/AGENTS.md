# Custom Agent Rules

## Core Development Methodology
- **Core Development Loop**: Every phase development must strictly follow the loop:
  1. **Planning (SDD)**: Define or review the System Design Document.
  2. **Implementation (Coding)**: Write and refine codebase modules.
  3. **Testing (Mock)**: Run comprehensive mocks and unit/integration tests.
  4. **Live Verification (Report)**: Conduct live verification and create QA Audit Reports.
  5. **Master Plan and Walkthrough Lock**: Update `MASTER_PLAN.md` status, checklist files, and create/update the walkthrough file to lock the phase.

## PDF Reading Rules
- **NEVER** use the `view_file` tool directly on PDF files (e.g., `*.pdf` files like `AI WEBSITE UPGRADE AGENCY PART 1 - Google Docs.pdf`). Doing so will crash the execution environment.
- Instead, always write and run a temporary Python script in the scratch directory using the `fitz` (PyMuPDF) library to inspect, search, or extract text/content from the PDF.
- Example template for extracting text using `fitz`:
  ```python
  import fitz  # PyMuPDF
  doc = fitz.open("path/to/file.pdf")
  for page_num in range(len(doc)):
      page = doc.load_page(page_num)
      text = page.get_text()
      print(f"--- Page {page_num + 1} ---")
      print(text)
  ```
