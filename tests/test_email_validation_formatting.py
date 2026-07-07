import pytest
from agents.email.email_contracts import (
    GeneratedEmailDraft,
    ValidatedEmailDraft,
    ValidationReportContract
)
from agents.email.email_validator import EmailValidator
from agents.email.output_formatter import OutputFormatter
from agents.email.metadata_generator import MetadataGenerator

def test_validator_missing_structural_elements():
    # 1. Missing Greeting
    draft_1 = GeneratedEmailDraft(
        subject="Upgrade proposal",
        body="We reviewed your website. Best regards, Website Agency",
        target_email="test@test.com"
    )
    with pytest.raises(ValueError) as exc_1:
        EmailValidator.validate_draft(draft_1)
    assert "Greeting block is missing" in str(exc_1.value)
    
    # 2. Missing CTA
    draft_2 = GeneratedEmailDraft(
        subject="Upgrade proposal",
        body="Hi John,\nWe reviewed your website. Best regards, Website Agency",
        target_email="test@test.com"
    )
    with pytest.raises(ValueError) as exc_2:
        EmailValidator.validate_draft(draft_2)
    assert "Call-To-Action (CTA)" in str(exc_2.value)
    
    # 3. Missing Closing
    draft_3 = GeneratedEmailDraft(
        subject="Upgrade proposal",
        body="Hi John,\nWe reviewed your website at http://proto.com. Website Agency",
        target_email="test@test.com"
    )
    with pytest.raises(ValueError) as exc_3:
        EmailValidator.validate_draft(draft_3)
    assert "closing block is missing" in str(exc_3.value)
    
    # 4. Missing Signature
    draft_4 = GeneratedEmailDraft(
        subject="Upgrade proposal",
        body="Hi John,\nWe reviewed your website at http://proto.com. Best regards,",
        target_email="test@test.com"
    )
    with pytest.raises(ValueError) as exc_4:
        EmailValidator.validate_draft(draft_4)
    assert "Signature block is missing" in str(exc_4.value)

def test_validator_success_and_report():
    draft = GeneratedEmailDraft(
        subject="Upgrade proposal",
        body="Hi John,\nWe reviewed your website at http://proto.com.\nBest regards,\nWebsite Agency",
        target_email="test@test.com"
    )
    validated, report = EmailValidator.validate_draft(draft)
    assert report.status == "PASS"
    assert report.structural_validation == "PASS"
    assert report.personalization_validation == "PASS"
    assert len(report.errors) == 0

def test_output_formatter_spacing_normalization():
    validated = ValidatedEmailDraft(
        subject="Subject",
        body="   Hi John,   \n\n\n\n   Body line.   \n\n   Best regards,   \n\n   Website Agency   ",
        target_email="test@test.com"
    )
    formatted = OutputFormatter.format_output(validated)
    assert formatted.text_body == "Hi John,\n\nBody line.\n\nBest regards,\n\nWebsite Agency"
    assert "<p style='margin: 0 0 1em 0;'>Hi John,</p>" in formatted.html_body
    assert "Website Agency" in formatted.html_body

def test_metadata_generator_sealing():
    validated = ValidatedEmailDraft(
        subject="Subject",
        body="Hi John,\nWe reviewed your website at http://proto.com.\nBest regards,\nWebsite Agency",
        target_email="test@test.com"
    )
    formatted = OutputFormatter.format_output(validated)
    
    report = ValidationReportContract(
        validation_id="test-uuid",
        status="PASS",
        checked_at="2026-07-06T00:00:00",
        structural_validation="PASS",
        personalization_validation="PASS",
        communication_validation="PASS",
        factual_validation="PASS",
        formatting_validation="PASS",
        overall_validation_result="PASS",
        errors=[]
    )
    
    meta, sealed = MetadataGenerator.generate_metadata(formatted, report)
    assert sealed.metadata.validation_status == "PASS"
    assert sealed.metadata.engine_version == "EMAIL-1.0"
    assert sealed.metadata.execution_id is not None
    assert sealed.metadata.validation_report.validation_id == "test-uuid"
