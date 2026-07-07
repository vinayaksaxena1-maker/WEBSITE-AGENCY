from datetime import datetime, timezone
from typing import Dict, Any

class CertificationGenerator:
    @staticmethod
    def generate_pie_certificate(overall_score: int) -> Dict[str, Any]:
        """
        Creates standard release certificate JSON.
        """
        if overall_score >= 95:
            level = "Level A+"
            status = "Enterprise Production Certified"
        elif overall_score >= 90:
            level = "Level A"
            status = "Production Ready"
        elif overall_score >= 80:
            level = "Level B"
            status = "Client Demonstration Ready"
        elif overall_score >= 70:
            level = "Level C"
            status = "Internal Testing Only"
        else:
            level = "Level D"
            status = "Development Only"
            
        return {
            "certificate_id": f"CERT-PIE-2026-{overall_score}",
            "certification_date": datetime.now(timezone.utc).isoformat(),
            "generator_version": "PIE-1.0",
            "architecture_version": "EDK-V7",
            "quality_grade": level,
            "production_status": status
        }
