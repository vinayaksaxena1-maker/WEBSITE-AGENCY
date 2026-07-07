import pytest
from agents.email.email_contracts import (
    GeneratedEmailDraft,
    ValidatedEmailDraft,
    ValidationReportContract,
    FinalEmailPackage
)
from agents.email.email_validator import EmailValidator
from agents.email.output_formatter import OutputFormatter
from agents.email.metadata_generator import MetadataGenerator

def test_pydantic_nested_schema_validation():
    draft = GeneratedEmailDraft(
        subject="Upgrade proposal for Fitsport - Redesign Redy",
        body="Hi Jane Doe,\n\nWe reviewed your website and noticed opportunities. Our audit scored it at 85/100. We built a custom prototype at http://proto.com for you.\n\nBest regards,\nWebsite Agency",
        target_email="jane@fitsport.com"
    )
    
    # 1. Validation Layer (8.9)
    validated, report = EmailValidator.validate_draft(draft)
    assert isinstance(report, ValidationReportContract)
    assert report.status == "PASS"
    assert report.overall_validation_result == "PASS"
    assert report.structural_validation == "PASS"
    assert report.personalization_validation == "PASS"
    assert report.communication_validation == "PASS"
    
    # 2. Output Formatting Layer (8.10)
    formatted = OutputFormatter.format_output(validated)
    
    # 3. Metadata Generation Layer (8.11) & Schema Specification (8.12)
    meta, sealed = MetadataGenerator.generate_metadata(formatted, report)
    assert isinstance(sealed, FinalEmailPackage)
    
    # Assert nested schemas conform to SDD-014 / 8.12 specifications
    assert sealed.metadata.engine_version == "EMAIL-1.0"
    assert sealed.metadata.validation_status == "PASS"
    
    # Processing Metadata checks
    assert sealed.metadata.processing_metadata.processing_status == "PASS"
    assert sealed.metadata.processing_metadata.completion_status == "SUCCESS"
    assert sealed.metadata.processing_metadata.execution_duration_sec == 0.01
    
    # Publication Metadata checks
    assert sealed.metadata.publication_metadata.publication_status == "PUBLISHED"
    assert sealed.metadata.publication_metadata.output_package_identifier is not None
