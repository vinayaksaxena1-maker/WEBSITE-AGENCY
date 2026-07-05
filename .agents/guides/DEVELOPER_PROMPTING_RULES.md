# Prompt Engineering & AI Development Masterclass (Hinglish)

Mera ek raw app idea hai jise main ek AI Coding Agent (jaise Antigravity, Claude Code, ya Cursor) ke zariya develop karwana chahta hoon. Isme raw idea ko ek highly structured, low-token consuming, aur compile-safe "Developer Prompt" me convert karne ke rules aur templates hain.

---

## 1. Chat Summary: Utsav & Learning Journey

### A. Token Ki Samasya Aur Solution (Token Problem & Code Splitting)
* **Ques:** Kya har bar command chalane par AI sabhi 1,600+ skills ko read karega aur tokens spend honge?
* **Ans:** Nahi! AI locally index search karta hai aur trigger words ke matching se keval 1-2 relevant skills hi load karta hai.
* **What I Learned:** AI ko kaam dene se pehle code ko choti modular files me split rakhna zaroori hai. Badi 2,800 lines ki file ke bajay 100 lines ki file load karne se direct 90% tokens bachte hain.

### B. No-Code File Locating (Zero-Token Local Search)
* **Ques:** Agar mujhe coding nahi aati aur main exact line number nahi dhoondh pata, toh kya karu?
* **Ans:** Aapko code copy-paste karne ki zaroorat nahi hai. Aap bas file path aur component name likh kar prompt dein, AI use locally locate kar lega.
* **What I Learned:** AI local PowerShell/bash search se bina API token kharch kiye code locate kar leta hai. Hame bas correct file name guide karna hota hai.

### C. 3-Step Perfect Prompt Formula
* **Ques:** Prompt likhne ka basic rules kya hai jisse AI jaldi samjhe aur tokens bhi safe rahein?
* **Ans:** Hamesha: (1) File/Component Path, (2) Specific action details (exact colors, sizes), aur (3) Safety directive ("baki code mat badalna") use karein.
* **What I Learned:** abstract words (*"thoda mota kar do"*) ke bajay exact pixels aur values dena best coding standard hai.

### D. Local Python Scripting (Zero-Token Refactoring)
* **Ques:** Kya code refactoring aur splitting karne me bohot tokens waste honge?
* **Ans:** Agar AI manually files likhega toh tokens jayenge, lekin iska solution local Python scripting hai.
* **What I Learned:** AI se ek local Python script (`split_components.py`) likhwayein aur use local computer par run karein. Isse complex code refactoring **0 API Token Cost** par ho jati hai.

### E. Chain-of-Thought (CoT) Prompting
* **Ques:** Brahm Muhurat aur Surya uday ke calculations ke liye logic kaise prompt karein?
* **Ans:** AI ko directly code likhne ke bajay logic ko step-1, step-2, step-3 me break karke thinking process explain karne ko boleise.
* **What I Learned:** Prompt ke rules ya instructions me *"Let's think step-by-step"* likhne se AI bina error ke correct coding aur calculations output karta hai.

### F. Few-Shot Prompting
* **Ques:** Quality translation (Excellent -> Shubh) ke formatting rules ko kaise prompt karein?
* **Ans:** Rules likhne ke bajay prompt me 2-3 input-output examples ka bracket `<Examples>` bana kar dein.
* **What I Learned:** 3 examples dekh kar AI formatting aur custom dictionary rules ko instantly grasp kar leta hai bina token waste kiye.

### G. Global Rule & Toggle Mode (AGENTS.md)
* **Ques:** Kya AI ke response style ko default short developer mode me rakh sakte hain aur sikhne ke liye switch off kar sakte hain?
* **Ans:** Haan! Global file `C:\Users\user\.gemini\config\AGENTS.md` me instructions likh kar toggling config set kar sakte hain.
* **What I Learned:** Custom rules se hum toggle bana sakte hain: *"Developer Mode: Off"* bol kar aaram se details me sikh sakte hain, aur *"Developer Mode: On"* bol kar direct code outputs le sakte hain.

---

## 2. 🎯 No-Code Developer Prompt Pattern

Bhavishya me prompts likhne ke liye aap is pattern ko yaad rakhein aur use karein:

```xml
<Context>
  Hum [Project Name] me [Feature/Screen Name] par kaam kar rahe hain.
</Context>

<Code_to_edit>
  File: [File Name and Path, e.g., src/components/ChaughadiyaRing.tsx]
  Component: [Component name or area to change, e.g., renderLabel function]
</Code_to_edit>

<Rules>
  1. [Jo cheez nahi badalni hai, e.g., default styles ko unchanged rakhein]
  2. AI pehle step-by-step logic calculate karega.
  3. AI bina kisi explanation ke keval code block output karega.
</Rules>

<Instructions>
  [Kya naya change karna hai, e.g., active hora ka size 18px karein aur bold style lagayein]
</Instructions>
```
