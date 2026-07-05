import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.email_validation.syntax_validator import SyntaxValidator
from agents.email_validation.dns_validator import DNSValidator
from agents.email_validation.mx_validator import MXValidator
from agents.email_validation.disposable_detector import DisposableDetector
from agents.email_validation.role_detector import RoleDetector
from agents.email_validation.quality_score import QualityScoreCalculator
from agents.email_validation.confidence_engine import ConfidenceEngine
from agents.email_validation.email_validation_agent import EmailValidationAgent

# ---------------------------------------------------------
# Syntax Validator Tests
# ---------------------------------------------------------
def test_syntax_validator():
    assert SyntaxValidator.validate("test@company.com") is True
    assert SyntaxValidator.validate("test.name+alias@sub.domain.co.uk") is True
    assert SyntaxValidator.validate("test@company.c") is False  # TLD too short
    assert SyntaxValidator.validate("test@company") is False  # Missing TLD
    assert SyntaxValidator.validate("testcompany.com") is False  # Missing @
    assert SyntaxValidator.validate("test@com@pany.com") is False  # Multiple @
    assert SyntaxValidator.validate("test @company.com") is False  # Whitespace
    assert SyntaxValidator.validate("") is False

# ---------------------------------------------------------
# DNS Validator Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_dns_validator_success():
    with patch("socket.gethostbyname", return_value="1.2.3.4"):
        assert await DNSValidator.validate_domain("google.com") is True

@pytest.mark.asyncio
async def test_dns_validator_failure():
    with patch("socket.gethostbyname", side_effect=Exception("Unknown Host")):
        assert await DNSValidator.validate_domain("nonexistent-domain-xyz.com") is False

# ---------------------------------------------------------
# MX Validator Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_mx_validator_success():
    mock_run = MagicMock()
    mock_run.stdout = "google.com mail exchanger = 10 smtp.google.com"
    with patch("subprocess.run", return_value=mock_run):
        assert await MXValidator.validate_mx("google.com") is True

@pytest.mark.asyncio
async def test_mx_validator_failure():
    mock_run = MagicMock()
    mock_run.stdout = "nonexistent-domain-xyz.com find nothing"
    with patch("subprocess.run", return_value=mock_run):
        assert await MXValidator.validate_mx("nonexistent-domain-xyz.com") is False

# ---------------------------------------------------------
# Disposable Detector Tests
# ---------------------------------------------------------
def test_disposable_detector():
    assert DisposableDetector.is_disposable("mailinator.com") is True
    assert DisposableDetector.is_disposable("tempmail.com") is True
    assert DisposableDetector.is_disposable("google.com") is False
    assert DisposableDetector.is_disposable("") is False

# ---------------------------------------------------------
# Role Detector Tests
# ---------------------------------------------------------
def test_role_detector():
    assert RoleDetector.is_role_based("info@company.com") is True
    assert RoleDetector.is_role_based("support@sub.domain.com") is True
    assert RoleDetector.is_role_based("john.doe@company.com") is False
    assert RoleDetector.is_role_based("") is False

# ---------------------------------------------------------
# Quality Score Calculator Tests
# ---------------------------------------------------------
def test_quality_score_calculator():
    # Perfect: matching domain, valid MX, non-role
    score = QualityScoreCalculator.calculate(
        email="hello@agency.com",
        is_syntax_valid=True,
        is_dns_valid=True,
        is_mx_valid=True,
        is_disposable=False,
        is_role_based=False,
        website_domain="https://agency.com"
    )
    assert score == 100

    # Role Email: matching domain, but role-based
    score = QualityScoreCalculator.calculate(
        email="info@agency.com",
        is_syntax_valid=True,
        is_dns_valid=True,
        is_mx_valid=True,
        is_disposable=False,
        is_role_based=True,
        website_domain="https://agency.com"
    )
    assert score == 60

    # Verified Generic: valid MX, generic domain
    score = QualityScoreCalculator.calculate(
        email="john@gmail.com",
        is_syntax_valid=True,
        is_dns_valid=True,
        is_mx_valid=True,
        is_disposable=False,
        is_role_based=False,
        website_domain="https://agency.com"
    )
    assert score == 80

    # Business Email: valid MX, non-matching business domain
    score = QualityScoreCalculator.calculate(
        email="john@partner-agency.com",
        is_syntax_valid=True,
        is_dns_valid=True,
        is_mx_valid=True,
        is_disposable=False,
        is_role_based=False,
        website_domain="https://agency.com"
    )
    assert score == 90

    # Questionable: DNS/MX missing
    score = QualityScoreCalculator.calculate(
        email="john@partner-agency.com",
        is_syntax_valid=True,
        is_dns_valid=False,
        is_mx_valid=False,
        is_disposable=False,
        is_role_based=False,
        website_domain="https://agency.com"
    )
    assert score == 30

    # Invalid: disposable domain
    score = QualityScoreCalculator.calculate(
        email="john@mailinator.com",
        is_syntax_valid=True,
        is_dns_valid=True,
        is_mx_valid=True,
        is_disposable=True,
        is_role_based=False,
        website_domain="https://agency.com"
    )
    assert score == 0

# ---------------------------------------------------------
# Confidence Engine Tests
# ---------------------------------------------------------
def test_confidence_engine():
    classification, confidence, action = ConfidenceEngine.get_classification_and_action(100, False)
    assert classification == "Premium"
    assert confidence == 1.0
    assert action == "Proceed Immediately"

    classification, confidence, action = ConfidenceEngine.get_classification_and_action(0, True)
    assert classification == "Temporary"
    assert confidence == 0.0
    assert action == "Reject"

# ---------------------------------------------------------
# Agent Orchestrator Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_email_validation_agent_orchestration_success():
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Mock Lead SearchLead
    mock_lead = MagicMock()
    mock_lead.id = 1
    mock_lead.domain = "company.com"
    mock_lead.status = "EXTRACTED"
    
    # Mock Contact
    mock_contact = MagicMock()
    mock_contact.lead_id = 1
    mock_contact.primary_email = "john@company.com"
    mock_contact.secondary_email = "info@company.com"
    
    mock_result = MagicMock()
    # First: lead existence verify. Second: contact record fetch. Third: lead reload. Fourth: existing validation checks.
    mock_result.scalars.return_value.first.side_effect = [mock_lead, mock_contact, mock_lead, None]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.email_validation.email_validation_agent.db_manager") as mock_db_mgr, \
         patch("agents.email_validation.email_validation_agent.redis_manager", mock_redis), \
         patch("agents.email_validation.email_validation_agent.event_bus", mock_event_bus), \
         patch("socket.gethostbyname", return_value="1.2.3.4"), \
         patch("subprocess.run", return_value=MagicMock(stdout="mail exchanger = 10 smtp.company.com")):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = EmailValidationAgent()
        report = await agent.validate_lead_emails(lead_id=1, url="company.com")
        
        assert report["lead_id"] == 1
        assert report["domain"] == "company.com"
        assert report["success"] is True
        assert report["email"] == "john@company.com"  # prefers perfect match (john@company.com has score 100 vs info@ has score 60)
        assert report["quality_score"] == 100
        
        assert mock_lead.status == "VALIDATED"
        assert mock_session.add.called
        assert mock_redis.push_to_queue.called
        assert mock_event_bus.publish.called

@pytest.mark.asyncio
async def test_email_validation_agent_orchestration_failure():
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Mock Lead SearchLead
    mock_lead = MagicMock()
    mock_lead.id = 2
    mock_lead.domain = "company-bad.com"
    mock_lead.status = "EXTRACTED"
    
    # Mock Contact with disposable email
    mock_contact = MagicMock()
    mock_contact.lead_id = 2
    mock_contact.primary_email = "john@mailinator.com"
    mock_contact.secondary_email = ""
    
    mock_result = MagicMock()
    # First: lead existence verify. Second: contact record fetch. Third: lead reload. Fourth: existing validation checks.
    mock_result.scalars.return_value.first.side_effect = [mock_lead, mock_contact, mock_lead, None]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.email_validation.email_validation_agent.db_manager") as mock_db_mgr, \
         patch("agents.email_validation.email_validation_agent.redis_manager", mock_redis), \
         patch("agents.email_validation.email_validation_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = EmailValidationAgent()
        report = await agent.validate_lead_emails(lead_id=2, url="company-bad.com")
        
        assert report["lead_id"] == 2
        assert report["domain"] == "company-bad.com"
        assert report["success"] is False
        assert report["quality_score"] == 0
        
        assert mock_lead.status == "INVALID_EMAIL"
        assert mock_session.add.called
        assert not mock_redis.push_to_queue.called
        assert mock_event_bus.publish.called
