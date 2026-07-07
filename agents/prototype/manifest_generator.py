import json
from typing import Dict, Any

class ManifestGenerator:
    @staticmethod
    def generate_manifest(metadata: Dict[str, Any], output_path: str) -> bool:
        """
        Generates standard manifest.json metadata file.
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
            return True
        except Exception:
            return False
