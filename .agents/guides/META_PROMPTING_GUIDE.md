# Meta-Prompting Guide for AI App Creators (Hinglish)

Agar aapke paas koi raw app idea (कच्चा विचार) hai aur aap ChatGPT ya Gemini se ek highly optimized, structured "Developer Prompt" generate karwana chahte hain (jise aap Antigravity/Cursor/Claude Code jaise coding agents ko de sakein), toh aap is **Meta-Prompt** ka use kar sakte hain.

---

## 1. Meta-Prompt Template (Copy-Paste)

Kisi bhi dusre AI model (jaise ChatGPT/Gemini) me ye text copy karein aur bracket `[...]` ke andar apna raw idea likh kar enter daba dein:

```text
Act as an expert AI Prompt Engineer specializing in developer-level app generation. 

Mera ek raw app idea hai jise main ek AI Coding Agent (jaise Antigravity, Claude Code, ya Cursor) ke zariya develop karwana chahta hoon. Aapka kaam mere raw idea ko ek highly structured, low-token consuming, aur compile-safe "Developer Prompt" me convert karna hai.

Aapke dwara generate kiye gaye prompt me ye sections hone chahiye:
1. [CONTEXT]: Project ka deep background aur use case kya hai.
2. [TECH STACK]: Kaun si languages aur libraries use honi chahiye (best recommendations).
3. [ARCHITECTURAL RULES]: Code-splitting, modular files, aur state management ke rules.
4. [FUNCTIONAL REQUIREMENTS]: Agents ya component wise features ka detail description.
5. [PHASED DEVELOPMENT (MVP)]: Pehle kya banana hai aur baad me kya (step-by-step).
6. [SAFETY & ERROR HANDLING]: API failures, edge cases, aur rate limits ko handle karne ke guidelines.

Mera raw app idea ye hai:
"[Yahan apna idea likhein, e.g., mujhe ek multi-agent lead gen tool banana hai]"

Generate the structured developer prompt based on this.
```

---

## 2. ChatGPT/Gemini Se Output Milne Ke Baad Kya Karein?

1. **Review & Refine:** ChatGPT/Gemini jo output dega, use padhein. Agar aapko koi library change karni hai, toh update karein.
2. **Coding Agent Ko Provide Karein:** Us output ko copy karke directly mujhe (ya kisi bhi coding agent ko) pehli chat me de dein.
3. **Phased Development:** AI ko step-by-step rules ke mutabik execution complete karne ki permission dein.
