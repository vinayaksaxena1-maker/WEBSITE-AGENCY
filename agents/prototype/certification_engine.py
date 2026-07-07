class CertificationEngine:
    @staticmethod
    def get_certification_level(overall_score: int) -> str:
        """
        Determines certification label based on score ranges.
        """
        if overall_score >= 95:
            return "Enterprise Certified"
        elif overall_score >= 90:
            return "Production Ready"
        elif overall_score >= 80:
            return "Client Presentation Ready"
        elif overall_score >= 70:
            return "Requires Minor Improvements"
        return "Rejected"
