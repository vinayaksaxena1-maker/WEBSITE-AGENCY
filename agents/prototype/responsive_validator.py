from typing import Dict, Any, List

class ResponsiveValidator:
    @staticmethod
    def validate_coverage(blueprint: Dict[str, Any]) -> tuple[int, str]:
        """
        Validates completeness checking all 7 viewports are defined.
        """
        required_keys = ["Desktop XL", "Desktop", "Laptop", "Tablet", "Mobile Large", "Mobile", "Small Mobile"]
        missing = [k for k in required_keys if k not in blueprint]
        
        if missing:
            return 100 - (len(missing) * 15), f"FAILED: Missing breakpoint configurations: {', '.join(missing)}"
            
        return 100, "PASSED"
