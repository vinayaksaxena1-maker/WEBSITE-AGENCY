import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.scoring.scoring_calculator import ScoringCalculator
from agents.scoring.business_value_calculator import BusinessValueCalculator
from agents.scoring.scoring_agent import ScoringAgent
from agents.scoring.scoring_models import LeadScore
from agents.search.search_models import SearchLead

def test_scoring_calculator_optimized():
    calculator = ScoringCalculator()
    
    # Mock audit with full scores (no deficiencies)
    mock_audit = MagicMock()
    mock_audit.design_score = 100
    mock_audit.mobile_score = 100
    mock_audit.speed_score = 100
    mock_audit.seo_score = 100
    mock_audit.trust_score = 100
    mock_audit.summary = "Website is highly optimized."
    
    score, opportunities = calculator.calculate_lead_score(mock_audit)
    assert score == 0
    assert len(opportunities) == 0

def test_scoring_calculator_unoptimized():
    calculator = ScoringCalculator()
    
    # Mock audit with total deficiencies
    mock_audit = MagicMock()
    mock_audit.design_score = 30
    mock_audit.mobile_score = 50
    mock_audit.speed_score = 40
    mock_audit.seo_score = 45
    mock_audit.trust_score = 40
    mock_audit.summary = "Audit reveals key modernization opportunities: SSL invalid/missing"
    
    score, opportunities = calculator.calculate_lead_score(mock_audit)
    
    # Deficiencies additions:
    # design < 50 (+30) -> Old Website Design
    # mobile < 70 (+25) -> Mobile Responsiveness Issues
    # speed < 60 (+20) -> Performance Problems
    # seo < 70 (+15) -> SEO Problems
    # trust < 70 (+10) -> Trust Issues
    # seo < 50 or design < 40 (+10) -> Broken Navigation
    # design < 60 (+10) -> Poor CTA Placement
    # design < 50 (+15) -> Outdated Branding
    # SSL invalid (+10) -> No SSL
    # mobile < 80 or design < 80 (+10) -> Accessibility Problems
    # Total sum is 30+25+20+15+10+10+10+15+10+10 = 155, capped at 100
    assert score == 100
    assert "Old Website Design" in opportunities
    assert "Mobile Responsiveness Issues" in opportunities
    assert "No SSL" in opportunities

def test_business_value_calculator():
    calculator = BusinessValueCalculator()
    
    # Mock audit and profile for Hospital (Multiplier 1.5)
    mock_audit = MagicMock()
    mock_audit.audit_score = 50
    mock_audit.trust_score = 60
    
    mock_profile = MagicMock()
    mock_profile.industry = "Hospital"
    mock_profile.confidence = 0.90
    
    lead_score = 80
    
    # Website Deficiencies = (100 - 50) / 100 = 0.5
    # Niche Confidence = 0.90
    # Industry Multiplier = 1.5
    # Contact Multiplier = 1.2 (trust_score >= 50)
    # Lead Score Factor = 80 / 100 = 0.8
    # BVI = 0.5 * 0.90 * 1.5 * 1.2 * 0.8 = 0.648
    bvi = calculator.calculate_business_value_index(mock_audit, mock_profile, lead_score)
    assert bvi == 0.648

    # Test Publisher (Multiplier 0.8) and low trust_score
    mock_profile.industry = "Publisher"
    mock_audit.trust_score = 30 # contact multiplier = 0.8
    # BVI = 0.5 * 0.90 * 0.8 * 0.8 * 0.8 = 0.2304
    bvi = calculator.calculate_business_value_index(mock_audit, mock_profile, lead_score)
    assert bvi == 0.2304

@pytest.mark.asyncio
async def test_scoring_agent_orchestration():
    # Setup context mocks for SQL session commits and Redis enqueuing
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session.add = MagicMock()
    
    # Mock SearchLead
    mock_lead = MagicMock()
    mock_lead.id = 1
    mock_lead.domain = "test-lead.com"
    mock_lead.status = "CLASSIFIED"
    
    # Mock Audit
    mock_audit = MagicMock()
    mock_audit.lead_id = 1
    mock_audit.audit_score = 60
    mock_audit.seo_score = 60
    mock_audit.mobile_score = 60
    mock_audit.speed_score = 60
    mock_audit.trust_score = 60
    mock_audit.design_score = 60
    mock_audit.summary = ""
    
    # Mock BusinessProfile
    mock_profile = MagicMock()
    mock_profile.lead_id = 1
    mock_profile.industry = "Real Estate"
    mock_profile.confidence = 0.95
    
    mock_result = MagicMock()
    # First verify existence, second audit, third profile, fourth check existing score, fifth update lead status
    mock_result.scalars.return_value.first.side_effect = [
        mock_lead,          # verify lead existence
        mock_audit,         # fetch audit
        mock_profile,       # fetch profile
        None,               # check existing lead score
        mock_lead           # reload lead object inside transaction
    ]
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = MagicMock()
    mock_event_bus.publish = AsyncMock()
    
    with patch("agents.scoring.scoring_agent.db_manager") as mock_db_mgr, \
         patch("agents.scoring.scoring_agent.redis_manager", mock_redis), \
         patch("agents.scoring.scoring_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = ScoringAgent()
        report = await agent.score_lead(lead_id=1, url="test-lead.com")
        
        assert report["lead_id"] == 1
        assert report["domain"] == "test-lead.com"
        assert report["lead_score"] > 0
        assert report["priority_level"] in ["Low Priority", "Medium Priority", "High Priority", "Premium Lead"]
        assert report["business_value_index"] > 0
        
        assert mock_session.add.called
        assert mock_redis.push_to_queue.called
        assert mock_event_bus.publish.called
