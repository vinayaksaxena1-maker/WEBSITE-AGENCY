import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.search.domain_filter import domain_filter
from agents.search.scraper_service import DuckDuckGoScraper
from agents.search.search_agent import SearchAgent

def test_domain_normalization():
    assert domain_filter.normalize_url("https://www.google.com/search?q=123") == "google.com"
    assert domain_filter.normalize_url("http://sub.domain.co.uk/index.html") == "sub.domain.co.uk"
    assert domain_filter.normalize_url("www.test-site.org") == "test-site.org"

def test_domain_validation():
    assert domain_filter.is_valid_domain("google.com") is True
    assert domain_filter.is_valid_domain("localhost") is False
    assert domain_filter.is_valid_domain("127.0.0.1") is False

def test_domain_blacklist():
    assert domain_filter.is_blacklisted("facebook.com") is True
    assert domain_filter.is_blacklisted("sub.yelp.com") is True
    assert domain_filter.is_blacklisted("my-agency.com") is False

def test_domain_pipeline_validate():
    assert domain_filter.validate("https://www.facebook.com/my-page") == ""
    assert domain_filter.validate("https://127.0.0.1/admin") == ""
    assert domain_filter.validate("https://www.my-clean-clinic.com/index") == "my-clean-clinic.com"

@pytest.mark.asyncio
async def test_scraper_mock_fallback():
    scraper = DuckDuckGoScraper()
    # Patch urllib to throw exception and force full mock fallback execution
    with patch("urllib.request.urlopen", side_effect=Exception("Simulated blocking")):
        urls = await scraper.search("Schools Delhi", limit=10)
        assert len(urls) >= 10
        # Mocked blacklist urls should now be in returned array
        assert any("facebook.com" in url for url in urls)

@pytest.mark.asyncio
async def test_search_agent_pipeline():
    # Construct async context manager mocks for session and begin transactions
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    
    with patch("agents.search.search_agent.db_manager") as mock_db_mgr, \
         patch("agents.search.search_agent.redis_manager", mock_redis):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = SearchAgent()
        report = await agent.execute("Schools", "Delhi", limit=60)
        
        assert report["status"] in ["PASS", "FAIL"]
        assert report["niche"] == "Schools"
        assert report["geographic_target"] == "Delhi"
        assert len(report["stored_leads"]) > 0
        assert mock_redis.push_to_queue.called
