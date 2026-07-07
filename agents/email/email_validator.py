import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from agents.email.email_contracts import GeneratedEmailDraft, ValidatedEmailDraft, ValidationReportContract

class EmailValidator:
    @staticmethod
    def validate_draft(generated_email: GeneratedEmailDraft) -> Tuple[ValidatedEmailDraft, ValidationReportContract]:
        """
        Verifies draft satisfies structural, personalization, factual, and communication quality checks.
        """
        subject = generated_email.subject.strip()
        body = generated_email.body.strip()
        
        errors = []
        
        # 1. Structural Checks
        if not subject:
            errors.append("Subject line is missing.")
        if not body:
            errors.append("Email body is missing.")
            
        greeting_pattern = r"^(hi|hello|dear|good\s+morning|good\s+afternoon)\b"
        if not re.search(greeting_pattern, body, re.IGNORECASE):
            errors.append("Greeting block is missing or invalid.")
            
        cta_pattern = r"(https?://\S+|prototype|preview|demo)"
        if not re.search(cta_pattern, body, re.IGNORECASE):
            errors.append("Call-To-Action (CTA) link or reference is missing.")
            
        closing_pattern = r"(best regards|sincerely|regards|warmly|thanks|thank you)"
        if not re.search(closing_pattern, body, re.IGNORECASE):
            errors.append("Professional closing block is missing.")
            
        signature_pattern = r"(website agency|redesign redy|agency team|outreach team)"
        if not re.search(signature_pattern, body, re.IGNORECASE):
            errors.append("Signature block is missing.")
            
        # 2. Personalization & Placeholders Check
        placeholder_pattern = r"\{[a-zA-Z_0-9]+\}|\[[a-zA-Z_0-9\s]+\]"
        if re.search(placeholder_pattern, subject):
            errors.append("Subject contains unresolved placeholders.")
        if re.search(placeholder_pattern, body):
            errors.append("Body contains unresolved placeholders.")
            
        is_valid = len(errors) == 0
        
        report = ValidationReportContract(
            validation_id=str(uuid.uuid4()),
            status="PASS" if is_valid else "FAIL",
            checked_at=datetime.now(timezone.utc).isoformat(),
            structural_validation="PASS" if not any(x in str(errors) for x in ["Subject", "body", "Greeting", "Call-To-Action", "closing", "Signature"]) else "FAIL",
            personalization_validation="PASS" if "placeholder" not in str(errors) else "FAIL",
            communication_validation="PASS" if "closing" not in str(errors) and "Greeting" not in str(errors) else "FAIL",
            factual_validation="PASS" if "CTA" not in str(errors) else "FAIL",
            formatting_validation="PASS" if is_valid else "FAIL",
            overall_validation_result="PASS" if is_valid else "FAIL",
            errors=errors
        )
        
        if not is_valid:
            raise ValueError(f"Email validation failed: {', '.join(errors)}")
            
        validated_dto = ValidatedEmailDraft(
            subject=subject,
            body=body,
            target_email=generated_email.target_email
        )
        return validated_dto, report
