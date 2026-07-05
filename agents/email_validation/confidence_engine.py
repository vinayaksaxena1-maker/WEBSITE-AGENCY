class ConfidenceEngine:
    @staticmethod
    def get_classification_and_action(quality_score: int, is_disposable: bool) -> tuple[str, float, str]:
        """
        Returns a tuple of (classification, confidence_score, recommended_action).
        """
        if quality_score == 0:
            classification = "Temporary" if is_disposable else "Invalid"
            confidence = 0.0
            action = "Reject"
        elif quality_score == 30:
            classification = "Questionable"
            confidence = 0.3
            action = "Proceed with Lower Priority"
        elif quality_score == 60:
            classification = "Role-based"
            confidence = 0.6
            action = "Proceed with Generic Template"
        elif quality_score == 80:
            classification = "Verified"
            confidence = 0.8
            action = "Proceed"
        elif quality_score == 90:
            classification = "Business Verified"
            confidence = 0.9
            action = "Proceed"
        elif quality_score == 100:
            classification = "Premium"
            confidence = 1.0
            action = "Proceed Immediately"
        else:
            # Fallback
            classification = "Questionable"
            confidence = 0.3
            action = "Proceed with Lower Priority"
            
        return classification, confidence, action
