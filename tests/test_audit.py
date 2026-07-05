import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.audit.interfaces import IBrowserEngine
from agents.audit.browser_engine import UrllibBrowserEngine
from agents.audit.audit_services import AuditService
from agents.audit.audit_rules import AuditRules
from agents.audit.scoring_strategies import (
    SeoScoreStrategy,
    MobileScoreStrategy,
    SpeedScoreStrategy,
    TrustScoreStrategy,
    DesignScoreStrategy
)
from agents.audit.audit_agent import AuditAgent

def test_seo_scoring_strategy():
    strategy = SeoScoreStrategy()
    
    # Test optimized page
    page_a = {
        "html": "<html><head><title>Optimal Hospital Services</title><meta name='description' content='Best healthcare in town'></head><body><h1>Main Services</h1><h2>Department A</h2></body></html>"
    }
    assert strategy.evaluate(page_a) == 100
    
    # Test unoptimized page (short title, missing meta, multiple h1s, missing h2/h3)
    page_b = {
        "html": "<html><head><title>Bad</title></head><body><h1>Title 1</h1><h1>Title 2</h1></body></html>"
    }
    # Title too short: +15, No Meta Description: +0, Multiple H1s: +10, No H2/H3: +0 => Total 25
    assert strategy.evaluate(page_b) == 25

def test_mobile_scoring_strategy():
    strategy = MobileScoreStrategy()
    
    # Test optimized mobile
    page_a = {
        "html": "<html><head><meta name='viewport' content='width=device-width'><style>@media (max-width: 600px) { body { display: flex; } }</style></head></html>"
    }
    assert strategy.evaluate(page_a) == 100
    
    # Test non-responsive page
    page_b = {
        "html": "<html><head></head></html>"
    }
    assert strategy.evaluate(page_b) == 0

def test_speed_scoring_strategy():
    strategy = SpeedScoreStrategy()
    
    assert strategy.evaluate({"response_time_ms": 300}) == 100
    assert strategy.evaluate({"response_time_ms": 1000}) == 75
    assert strategy.evaluate({"response_time_ms": 2500}) == 50
    assert strategy.evaluate({"response_time_ms": 4000}) == 25

def test_trust_scoring_strategy():
    strategy = TrustScoreStrategy()
    
    # Test fully trusted
    page_a = {
        "html": "<html><body><a href='/privacy-policy'>Privacy Policy</a><a href='tel:123'>Call Us</a></body></html>",
        "ssl_valid": True
    }
    assert strategy.evaluate(page_a) == 100
    
    # Test untrusted
    page_b = {
        "html": "<html><body></body></html>",
        "ssl_valid": False
    }
    assert strategy.evaluate(page_b) == 0

def test_design_scoring_strategy():
    strategy = DesignScoreStrategy()
    
    # Test good design layout
    page_a = {
        "html": "<header></header><main><a href='/book-now'>Book Appointment</a></main><footer></footer>"
    }
    assert strategy.evaluate(page_a) == 100
    
    # Test missing structure and CTAs
    page_b = {
        "html": "<body><p>Hello</p></body>"
    }
    assert strategy.evaluate(page_b) == 0

def test_audit_rules_weighting():
    rules = AuditRules()
    
    # Fully compliant page inputs containing flex styles to satisfy mobile layout checks
    parse_payload = {
        "html": "<html><head><title>Optimal Hospital Services</title><meta name='description' content='Care'><meta name='viewport'></head><header><main style='display: flex;'><h1>Title</h1><h2>H2</h2><a href='/book'>Book Now</a><a href='/privacy'>Privacy</a><a href='tel:1'>Call</a></main><footer></footer></html>",
        "response_time_ms": 200,
        "ssl_valid": True
    }
    scores = rules.calculate_scores(parse_payload)
    
    assert scores["audit_score"] == 100
    assert scores["seo_score"] == 100
    assert scores["schema_version"] == "1.0.0"
    assert scores["audit_rule_version"] == "1.0.0"
    assert "Website is highly optimized" in scores["summary"]

@pytest.mark.asyncio
async def test_urllib_browser_engine_failure_fallback():
    service = AuditService()
    
    # Patch the browser engine call to throw an error
    with patch.object(service.browser_engine, "fetch_url", side_effect=Exception("Connection Timeout")):
        # Should not crash but fallback to mock content
        data = await service.fetch_page_content("http://some-offline-target.com")
        assert "Mock Healthcare Provider" in data["html"]
        assert data["load_time_ms"] == 1200
        assert data["ssl_valid"] is False

@pytest.mark.asyncio
async def test_audit_agent_orchestrator():
    # Setup context mocks for SQL session commits and Redis enqueuing
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Re-fetch returns a mock lead object
    mock_lead = MagicMock()
    mock_lead.id = 1
    mock_lead.domain = "test-domain.com"
    mock_lead.status = "DISCOVERED"
    
    mock_result = MagicMock()
    # First call verifies existence, second checks duplicate, third handles lock updates
    mock_result.scalars.return_value.first.side_effect = [mock_lead, None, mock_lead]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.audit.audit_agent.db_manager") as mock_db_mgr, \
         patch("agents.audit.audit_agent.redis_manager", mock_redis), \
         patch("agents.audit.audit_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = AuditAgent()
        
        # Override crawler return data to assert scores in isolation
        with patch.object(agent.service, "fetch_page_content", return_value={
            "html": "<html><head><title>Optimal Hospital Services</title><meta name='description' content='Care'><meta name='viewport'></head><header><main style='display: flex;'><h1>Title</h1><h2>H2</h2><a href='/book'>Book Now</a><a href='/privacy'>Privacy</a><a href='tel:1'>Call</a></main><footer></footer></html>",
            "load_time_ms": 200,
            "response_time_ms": 200,
            "ssl_valid": True,
            "ssl_issuer": "Let's Encrypt",
            "ssl_expiry": "2030-01-01T00:00:00Z",
            "headers": {}
        }):
            report = await agent.audit_site(1, "test-domain.com")
            
            assert report["lead_id"] == 1
            assert report["domain"] == "test-domain.com"
            assert report["audit_score"] == 100
            assert report["metrics"]["seo"]["score"] == 100
            assert report["schema_version"] == "1.0.0"
            assert report["audit_rule_version"] == "1.0.0"
            
            assert mock_redis.push_to_queue.called
            assert mock_event_bus.publish.called
