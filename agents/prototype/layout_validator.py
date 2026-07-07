from typing import List, Dict, Any
from core.logger import logger

class LayoutValidator:
    @staticmethod
    def validate_and_repair(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validates page structures. Injects missing critical layout wrappers (header/footer).
        Sanitizes section names.
        """
        logger.info("LayoutValidator: Executing missing block rendering protections check...")
        repaired = [sec.copy() for sec in sections]

        # 1. Sanity filter: clean names
        for sec in repaired:
            name = sec.get("section", "block").strip()
            # Clean symbols or spaces
            sec["section"] = "".join(c for c in name if c.isalnum() or c in ("-", "_")).lower()

        section_names = {sec["section"] for sec in repaired}

        # 2. Header Auto-injection Protection
        if "header" not in section_names and "navigation" not in section_names:
            logger.warning("LayoutValidator: Missing Header section! Injecting header block.")
            repaired.insert(0, {"section": "header", "layout": "simple", "height": "auto"})

        # 3. Footer Auto-injection Protection
        if "footer" not in section_names:
            logger.warning("LayoutValidator: Missing Footer section! Injecting footer block.")
            repaired.append({"section": "footer", "layout": "simple"})

        return repaired
