from typing import List, Dict, Any
from core.logger import logger
from agents.prototype.component_library import COMPONENTS_LIBRARY

class ComponentSelector:
    @staticmethod
    def select_components(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Translates raw parsed DOM sections into cataloged standard UI components.
        Provides generic SectionComponent fallback for unknown tags.
        """
        logger.info("ComponentSelector: Mapping DOM sections to component specs...")
        selected = []

        for idx, sec in enumerate(sections):
            sec_type = sec.get("type", "section").lower()

            # Mapping matches
            if sec_type == "hero":
                comp = COMPONENTS_LIBRARY["HeroComponent"].copy()
            elif sec_type in ("services", "products", "features"):
                comp = COMPONENTS_LIBRARY["ServicesComponent"].copy()
            elif sec_type == "faq":
                comp = COMPONENTS_LIBRARY["FAQComponent"].copy()
            elif sec_type in ("testimonials", "reviews"):
                comp = COMPONENTS_LIBRARY["TestimonialsComponent"].copy()
            elif sec_type in ("contact", "form"):
                comp = COMPONENTS_LIBRARY["ContactFormComponent"].copy()
            elif sec_type == "header":
                comp = COMPONENTS_LIBRARY["HeaderComponent"].copy()
            elif sec_type == "footer":
                comp = COMPONENTS_LIBRARY["FooterComponent"].copy()
            else:
                # Invalid tag parsing recovery rule: fallback to generic SectionComponent
                logger.warning(f"ComponentSelector: Unmapped section '{sec_type}' encountered. Falling back to SectionComponent.")
                comp = COMPONENTS_LIBRARY["SectionComponent"].copy()
                comp["name"] = f"Custom{sec_type.capitalize()}SectionComponent"

            # Assign instance details
            comp["instance_id"] = f"{comp['name']}_{idx}"
            comp["order"] = idx
            selected.append(comp)

        return selected
