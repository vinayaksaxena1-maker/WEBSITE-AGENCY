from typing import List, Dict, Any
from core.logger import logger

# Layout section priority mappings
SEQUENCE_PRIORITIES = {
    "header": 0,
    "navigation": 1,
    "hero": 2,
    "about": 3,
    "services": 4,
    "features": 4,
    "products": 4,
    "testimonials": 5,
    "reviews": 5,
    "faq": 6,
    "contact": 7,
    "footer": 8
}

class SequenceSorter:
    @staticmethod
    def sort_sequence(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sorts page blocks/sections dynamically according to standard usability sequencing rules.
        """
        logger.info("SequenceSorter: Re-ordering layout sections sequence flow...")
        
        def get_priority(sec: Dict[str, Any]) -> int:
            name = sec.get("section", "services").lower()
            # fuzzy matches
            for k, val in SEQUENCE_PRIORITIES.items():
                if k in name:
                    return val
            return 4  # default to content priority level

        return sorted(sections, key=get_priority)
