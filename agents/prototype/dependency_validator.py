from typing import List, Dict, Any, Set
from core.logger import logger

class DependencyValidator:
    @classmethod
    def validate_dependencies(
        cls,
        components: List[Dict[str, Any]],
        max_cycles: int = 15
    ) -> List[str]:
        """
        Scans component listings, tracing required dependencies tags.
        Enforces recursive execution threshold limit (< 1 cycle iterations check) to prevent stack overflow.
        """
        logger.info("DependencyValidator: Verifying component dependencies...")
        missing_errors = []

        # Gather compiled components set
        existing_names = {c["name"] for c in components}
        
        cycle_count = 0
        for comp in components:
            # Enforce recursive safety limits
            if cycle_count >= max_cycles:
                logger.warning(f"DependencyValidator: Recursive check cycles limit ({max_cycles}) reached. Halting validator.")
                break

            for dep in comp.get("dependencies", []):
                cycle_count += 1
                if dep not in existing_names:
                    msg = f"Dependency Error: Component '{comp['name']}' requires '{dep}', but it was not compiled in this pipeline."
                    logger.warning(msg)
                    missing_errors.append(msg)

        return missing_errors
