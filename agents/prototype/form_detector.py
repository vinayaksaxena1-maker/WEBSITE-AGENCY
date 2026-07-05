from bs4 import BeautifulSoup
from typing import List, Dict, Any

class FormDetector:
    @staticmethod
    def detect_forms(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Locates and catalogs input forms, newsletter submissions, and quote forms.
        """
        forms = []
        form_elements = soup.find_all("form")
        
        # Fallback: scan for div blocks containing multiple input fields
        if not form_elements:
            divs = soup.find_all("div")
            for div in divs:
                inputs = div.find_all(["input", "textarea", "select"])
                if len(inputs) >= 2 and not div.find_parent("form"):
                    form_elements.append(div)

        for idx, f in enumerate(form_elements):
            f_id = f.get("id", f"form-{idx}")
            f_class = " ".join(f.get("class", [])).lower()
            
            inputs = f.find_all(["input", "textarea", "select", "button"])
            fields = []
            
            # Analyze fields
            for inp in inputs:
                inp_type = inp.get("type", inp.name.lower())
                inp_name = inp.get("name", inp.get("placeholder", ""))
                if inp_type in ["text", "email", "tel", "number", "select", "textarea", "checkbox"]:
                    fields.append({
                        "name": inp_name,
                        "type": inp_type
                    })
            
            # Categorize form
            form_type = "contact"
            text_str = f.get_text().lower()
            if "news" in f_class or "sub" in f_class or ("news" in text_str and len(fields) <= 2):
                form_type = "newsletter"
            elif "login" in f_class or "signin" in f_class:
                form_type = "login"
            elif "register" in f_class or "signup" in f_class:
                form_type = "registration"
            elif "search" in f_class or "search" in text_str:
                form_type = "search"
            elif "booking" in f_class or "reserve" in text_str:
                form_type = "booking"

            forms.append({
                "id": f_id,
                "type": form_type,
                "fields_count": len(fields),
                "fields": fields
            })

        return forms
