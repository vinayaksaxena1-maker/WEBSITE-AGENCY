# Prompting Guide for AI Token Savings (Hinglish)

AI coding assistant (Antigravity/Gemini) ke sath kaam karte waqt apne tokens ko bachane, cost kam karne aur response speed badhane ke liye ye ek complete guide hai.

---

## 1. Token Bachane ka Formula: 3-Step Prompt

Jab bhi aap koi command ya instruction dein, toh usme ye 3 cheezein zaroor likhein:

1. **File Path / Component Name:** File ka exact name aur location.
2. **Exact Action:** Kya change karna hai (specific line number ya function name ke sath).
3. **Safety Directive:** "Baki koi change nahi hoga" ya "Do not change anything else".

---

## 2. Examples (Good vs. Bad Prompts)

### ❌ Bad Prompt (Jisme high tokens spend hote hain aur time lagta hai)
> *"clock me jo city choose karne ka option hai usko design thoda change karo."*
* **Nuksan:** AI ko poore project me search chalana padega, multiple files load karni padengi, jisse search me hi hazaaron tokens waste ho jayenge.

###  Good Prompt (Jisme minimal tokens lagte hain aur task instant hota hai)
> *"File `src/components/CitySelector.tsx` me Dropdown container ka background color badal kar `#3B2314` kar do. Baki koi change nahi hoga."*
* **Fayda:** AI direct usi file ko kholega aur precise edit karega. 90% tokens ki bachat hogi!

---

## 3. Token Saving ke 5 Sunhere Niyam (Golden Rules)

1. **Code Splitting (Refactoring):**
   * Apne main components ko choti files me split rakhein (ideal size: <300 lines).
   * Har change me poori 2,800 lines ki file load karne ke bajay sirf choti target file (~100-200 lines) hi load hogi, jisse direct 90% input tokens bachenge.
2. **One Task at a Time (Ek baar me ek kaam):**
   * Ek hi prompt me 5 changes likhne ke bajay, ek-ek karke kaam karwayein. Isse active chat history aur memory clean rehti hai.
3. **Local Python Automation (Paython Scripting):**
   * Jab bhi bade refactoring ya code migration ka kaam ho, toh AI se code likhwane ke bajay AI se ek **local Python script** likhwayein aur use run karein. Isse local system par processing hogi aur **0 API tokens** kharch honge.
4. **Specific Values (Sateek Values):**
   * "Thoda dark kar do" ya "font badha do" bolne ke bajay exact hex color codes (jaise `#D4AF37`) aur sizes (jaise `font-size: 22px`) dein.
5. **New Chat Sessions (Chat ko Reset karna):**
   * Jab ek bada feature complete ho jaye, toh chat session ko reset ya new chat start karein taaki purana code context baar-bar AI ke input me na jaye.

---

## 4. IDE (VS Code / Cursor) Me Lines & Files Kaise Dhoondhein?

AI ko exact line number dene se tokens aur save hote hain. Aap unhe aise dhoondh sakte hain:
* **Ctrl + F (Find):** File khol kar target component/function ka naam likhein. Editor aapko line number dikha dega.
* **Ln / Col details:** Apne code cursor ko us line par le jayein aur editor ke bottom-right corner me line number check karein (Jaise: `Ln 945, Col 12`).
* **AI local search:** Agar aapko dhoondhne me aalas aa raha hai, toh AI ko bole ki *"local search se `HoraRing` ka line number pata karo"* - ye local command run karega jisme **0 tokens** lagte hain, aur aapko exact line number bata dega!
