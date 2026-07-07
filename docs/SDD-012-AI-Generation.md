# System Design Document (SDD-012)
## Phase 8.8 - AI Personalized Email Engine AI Generation Layer

This document details the design specifications, API endpoints, payload configurations, and rate-limiting throttling behaviors for the AI Generation Layer (8.8).

---

### 1. Architectural Position & REST Interface
The AI Generation Layer communicates with Google AI Studio using non-blocking asynchronous HTTP calls.
* **Client Library**: `httpx.AsyncClient` is utilized to prevent event loop blocking.
* **REST Endpoint**:
  `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}`
* **Request Method**: `POST`
* **JSON Request Payload Structure**:
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "<compiled_prompt>"
        }
      ]
    }
  ]
}
```

---

### 2. 12-Second Throttling Logic
To comply with the free tier limits (5 requests per minute), the layer implements a strict class-level rate limiter:
* **`asyncio.Lock()`**: Prevents race conditions when executing concurrent email generations.
* **Timestamp Tracking**: Tracks the timestamp of the last successful API request (`_last_call_time`).
* **Dynamic Backoff Delay**: Calculates the time difference: `elapsed = current_time - _last_call_time`. If `elapsed` < 12 seconds, execution is paused using `await asyncio.sleep(12.0 - elapsed)`.

---

### 3. Response Parsing & Structuring
The response returned by the REST API contains the generated text:
* Parse text content from `candidates[0].content.parts[0].text`.
* Split the output string to extract:
  - Subject line (matched via `Subject:` or first line).
  - Body content (everything following the subject).
* Seal the extracted parts into the `GeneratedEmailDraft` Pydantic DTO.
