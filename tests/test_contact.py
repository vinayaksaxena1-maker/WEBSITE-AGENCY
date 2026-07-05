import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.contact.normalizer import ContactNormalizer
from agents.contact.validator import ContactValidator
from agents.contact.email_extractor import EmailExtractor
from agents.contact.phone_extractor import PhoneExtractor
from agents.contact.social_extractor import SocialExtractor
from agents.contact.contact_parser import ContactParser
from agents.contact.contact_agent import ContactAgent

# ---------------------------------------------------------
# Normalizer Tests
# ---------------------------------------------------------
def test_normalizer_email():
    assert ContactNormalizer.normalize_email("  TEST@Domain.COM  ") == "test@domain.com"
    assert ContactNormalizer.normalize_email("") == ""

def test_normalizer_phone():
    assert ContactNormalizer.normalize_phone("  +1 (123) 456-7890  ") == "+11234567890"
    assert ContactNormalizer.normalize_phone("080-1234-5678") == "08012345678"
    assert ContactNormalizer.normalize_phone("abc") == ""
    assert ContactNormalizer.normalize_phone("") == ""

def test_normalizer_social():
    assert ContactNormalizer.normalize_social("facebook.com/my-page/") == "https://facebook.com/my-page"
    assert ContactNormalizer.normalize_social("http://Twitter.com/User?query=1") == "http://twitter.com/User"
    assert ContactNormalizer.normalize_social("") == ""

# ---------------------------------------------------------
# Validator Tests
# ---------------------------------------------------------
def test_validator_email():
    assert ContactValidator.validate_email("test@domain.com") is True
    assert ContactValidator.validate_email("invalid-email") is False
    assert ContactValidator.validate_email("") is False

def test_validator_phone():
    assert ContactValidator.validate_phone("+11234567890") is True
    assert ContactValidator.validate_phone("123456") is False  # too short
    assert ContactValidator.validate_phone("12345678901234567") is False  # too long
    assert ContactValidator.validate_phone("") is False

def test_validator_social():
    assert ContactValidator.validate_social("https://www.facebook.com/user", "facebook") is True
    assert ContactValidator.validate_social("https://twitter.com/user", "facebook") is False
    assert ContactValidator.validate_social("https://x.com/user", "twitter") is True
    assert ContactValidator.validate_social("", "linkedin") is False

def test_validator_determine_quality():
    # Complete: email + phone + social
    assert ContactValidator.determine_quality({
        "primary_email": "a@b.com",
        "phone": "+123456789",
        "facebook": "http://fb.com"
    }) == "Complete"
    
    # Email Only
    assert ContactValidator.determine_quality({
        "primary_email": "a@b.com"
    }) == "Email Only"

    # Phone Only
    assert ContactValidator.determine_quality({
        "phone": "+123456789"
    }) == "Phone Only"

    # Social Only
    assert ContactValidator.determine_quality({
        "facebook": "http://fb.com"
    }) == "Social Only"

    # No Contact
    assert ContactValidator.determine_quality({}) == "No Contact"

    # Partial: Email + Phone, no social
    assert ContactValidator.determine_quality({
        "primary_email": "a@b.com",
        "phone": "+123456789"
    }) == "Partial"

# ---------------------------------------------------------
# Extractor Tests
# ---------------------------------------------------------
def test_email_extractor():
    extractor = EmailExtractor()
    html = """
    <html>
      <body>
        <p>Send mail to <a href="mailto:info@agency.com">info@agency.com</a></p>
        <p>Or write to contact@agency.com</p>
        <p>This is a fake image test@agency.com.png</p>
        <script>var email = 'ignored@agency.com';</script>
      </body>
    </html>
    """
    emails = extractor.extract(html)
    assert "info@agency.com" in emails
    assert "contact@agency.com" in emails
    assert "ignored@agency.com" not in emails
    assert "test@agency.com.png" not in emails

def test_phone_extractor():
    extractor = PhoneExtractor()
    html = """
    <html>
      <body>
        <a href="tel:+1234567890">Call Us</a>
        <p>Phone: +44 20 7946 0958</p>
        <p>Fake: 123-456</p>
        <script>var p = '9999999999';</script>
      </body>
    </html>
    """
    phones = extractor.extract(html)
    assert "+1234567890" in phones
    assert "+44 20 7946 0958" in phones
    assert "123-456" not in phones
    assert "9999999999" not in phones

def test_social_extractor():
    extractor = SocialExtractor()
    html = """
    <html>
      <body>
        <a href="https://www.facebook.com/agency">FB</a>
        <a href="https://linkedin.com/company/agency">LinkedIn</a>
        <a href="//instagram.com/agency">Insta</a>
        <a href="/about-us">Internal Link</a>
      </body>
    </html>
    """
    socials = extractor.extract(html)
    assert "https://www.facebook.com/agency" in socials["facebook"]
    assert "https://linkedin.com/company/agency" in socials["linkedin"]
    assert "https://instagram.com/agency" in socials["instagram"]
    assert len(socials["twitter"]) == 0

# ---------------------------------------------------------
# Parser Tests
# ---------------------------------------------------------
def test_contact_parser_internal_links():
    parser = ContactParser()
    html = """
    <html>
      <body>
        <a href="/about-us">About</a>
        <a href="https://site.com/contact">Contact</a>
        <a href="https://external.com/about">External</a>
        <a href="/support.html">Support</a>
      </body>
    </html>
    """
    links = parser.extract_internal_links(html, "https://site.com")
    assert "https://site.com/about-us" in links
    assert "https://site.com/contact" in links
    assert "https://site.com/support.html" in links
    assert "https://external.com/about" not in links

def test_contact_parser_parse_site_data():
    parser = ContactParser()
    pages_content = {
        "https://site.com": "<html><body>Email: info@site.com <a href='https://fb.com/site'>FB</a></body></html>",
        "https://site.com/contact": "<html><body>Phone: +1 (123) 456-7890</body></html>"
    }
    data = parser.parse_site_data(pages_content, "https://site.com")
    assert data["primary_email"] == "info@site.com"
    assert data["phone"] == "+11234567890"
    assert data["facebook"] == "https://fb.com/site"
    assert data["status"] == "Complete"

# ---------------------------------------------------------
# Agent Orchestrator Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_contact_agent_orchestration_success():
    # Setup DB mocks
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Mock search lead
    mock_lead = MagicMock()
    mock_lead.id = 1
    mock_lead.domain = "test-site.com"
    mock_lead.status = "SCORED"
    
    mock_result = MagicMock()
    # verify existence (lead), transaction fetch lead (lead), existing contact (None)
    mock_result.scalars.return_value.first.side_effect = [mock_lead, mock_lead, None]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.contact.contact_agent.db_manager") as mock_db_mgr, \
         patch("agents.contact.contact_agent.redis_manager", mock_redis), \
         patch("agents.contact.contact_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        # Mock browser engine to return HTML containing email/phone
        mock_browser = AsyncMock()
        mock_browser.fetch_url.return_value = {
            "html": "<html><body>Email: test@test-site.com Phone: +1 123 456 7890</body></html>",
            "load_time_ms": 100,
            "response_time_ms": 50,
            "headers": {}
        }
        
        agent = ContactAgent(browser_engine=mock_browser)
        report = await agent.extract_contacts(lead_id=1, url="test-site.com")
        
        assert report["lead_id"] == 1
        assert report["domain"] == "test-site.com"
        assert report["success"] is True
        assert report["primary_email"] == "test@test-site.com"
        assert report["phone"] == "+11234567890"
        assert report["status"] == "Partial"  # Email + Phone, no Social
        
        assert mock_lead.status == "EXTRACTED"
        assert mock_session.add.called
        assert mock_redis.push_to_queue.called
        assert mock_event_bus.publish.called

@pytest.mark.asyncio
async def test_contact_agent_orchestration_failure():
    # Setup DB mocks
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Mock search lead
    mock_lead = MagicMock()
    mock_lead.id = 1
    mock_lead.domain = "test-site-fail.com"
    mock_lead.status = "SCORED"
    
    mock_result = MagicMock()
    # verify existence (lead), transaction fetch lead (lead), existing contact (None)
    mock_result.scalars.return_value.first.side_effect = [mock_lead, mock_lead, None]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.contact.contact_agent.db_manager") as mock_db_mgr, \
         patch("agents.contact.contact_agent.redis_manager", mock_redis), \
         patch("agents.contact.contact_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        # Mock browser engine to throw timeout/exception
        mock_browser = AsyncMock()
        mock_browser.fetch_url.side_effect = Exception("Connection Timeout")
        
        agent = ContactAgent(browser_engine=mock_browser)
        report = await agent.extract_contacts(lead_id=1, url="test-site-fail.com")
        
        assert report["lead_id"] == 1
        assert report["domain"] == "test-site-fail.com"
        assert report["success"] is False
        
        assert mock_lead.status == "NO_CONTACT"
        assert not mock_session.add.called
        assert not mock_redis.push_to_queue.called
        assert mock_event_bus.publish.called
