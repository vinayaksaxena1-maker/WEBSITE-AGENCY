import pytest
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from sqlalchemy import select
from agents.search.search_models import SearchLead
from agents.niche.niche_models import BusinessProfile
from agents.niche.theme_mapper import ThemeMapper
from agents.niche.classifier import RuleEngineClassifier, GeminiClassifier, HybridClassifier
from agents.niche.niche_agent import NicheAgent

def test_rule_engine_classifier_matches():
    classifier = RuleEngineClassifier()
    
    # Gym HTML content
    gym_html = "<html><body><h1>Welcome to Premium CrossFit Fitness</h1><p>Check out our weightlifting workouts and yoga coaching sessions.</p></body></html>"
    industry, confidence = classifier.classify(gym_html)
    assert industry == "Gym"
    assert confidence == 0.95

    # Hospital HTML content
    hospital_html = "<html><head><title>St. George General Hospital</title></head><body><p>We provide emergency healthcare, medical doctor consultation and patient care treatment.</p></body></html>"
    industry, confidence = classifier.classify(hospital_html)
    assert industry == "Hospital"
    assert confidence == 0.95

    # Unknown HTML content
    unknown_html = "<html><body><h1>Random Business</h1><p>We sell items here.</p></body></html>"
    industry, confidence = classifier.classify(unknown_html)
    assert industry == "Unknown"
    assert confidence == 0.0


def test_theme_mapper_recommendations():
    mapper = ThemeMapper()
    
    assert mapper.recommend_theme("Hospital") == "clinical_comfort"
    assert mapper.recommend_theme("Gym") == "energy_dynamic"
    assert mapper.recommend_theme("Law Firm") == "justice_executive"
    assert mapper.recommend_theme("Random Industry Name") == "corporate_edge"


@pytest.mark.asyncio
async def test_gemini_classifier_dummy_fallback():
    classifier = GeminiClassifier()
    
    # Mock settings.GEMINI_API_KEY to default dummy_gemini_key
    with patch("agents.niche.classifier.settings") as mock_settings:
        mock_settings.GEMINI_API_KEY = "dummy_gemini_key"
        industry, confidence = classifier.classify("<html><body>Fitness Gym</body></html>")
        
        assert industry == "Business"
        assert confidence == 0.50


@pytest.mark.asyncio
async def test_niche_agent_orchestration():
    # Setup database mocks
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Mock parent lead search
    mock_lead = MagicMock()
    mock_lead.id = 1
    mock_lead.domain = "test-gym-niche.com"
    mock_lead.status = "AUDITED"
    
    mock_result = MagicMock()
    # First call: check lead exists. Second call: check existing profile. Third call: reload lead object.
    mock_result.scalars.return_value.first.side_effect = [mock_lead, None, mock_lead]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.niche.niche_agent.db_manager") as mock_db_mgr, \
         patch("agents.niche.niche_agent.redis_manager", mock_redis), \
         patch("agents.niche.niche_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = NicheAgent()
        
        gym_html = "<html><body><h1>CrossFit Fitness Gym</h1></body></html>"
        result = await agent.detect_niche(lead_id=1, url="test-gym-niche.com", html_content=gym_html)
        
        assert result["lead_id"] == 1
        assert result["domain"] == "test-gym-niche.com"
        assert result["industry"] == "Gym"
        assert result["recommended_theme"] == "energy_dynamic"
        
        # Verify status update
        assert mock_lead.status == "CLASSIFIED"
        
        # Verify event bus published
        mock_event_bus.publish.assert_called_once_with("niche_detected", ANY)
        
        # Verify Redis enqueued
        mock_redis.push_to_queue.assert_called_once_with("scoring_queue", "test-gym-niche.com")
