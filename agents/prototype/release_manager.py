class ReleaseManager:
    @staticmethod
    def get_release_decision(overall_score: int) -> tuple[str, bool]:
        """
        Determines PASS/FAIL status based on score.
        """
        if overall_score >= 90:
            return "PASS", True
        return "FAIL", False
