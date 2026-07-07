import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from agents.prototype.quality_validator import QualityValidator
from agents.prototype.accessibility_checker import AccessibilityChecker
from agents.prototype.seo_checker import SEOChecker
from agents.prototype.performance_checker import PerformanceChecker
from agents.prototype.ux_checker import UXChecker
from agents.prototype.component_checker import ComponentChecker
from agents.prototype.quality_score import QualityScore
from agents.prototype.certification_engine import CertificationEngine
from agents.prototype.recommendation_engine import RecommendationEngine
from agents.prototype.quality_report import QualityReport
from agents.prototype.quality_analyzer import QualityAnalyzer
from agents.prototype.prototype_models import PrototypeQuality

# ---------------------------------------------------------
# Checker Units Tests
# ---------------------------------------------------------
def test_individual_checkers():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <meta name="description" content="Meta Description block.">
        <link rel="canonical" href="https://example.com">
    </head>
    <body>
        <header></header>
        <nav aria-label="Main nav"><a href="#">Link</a></nav>
        <button class="btn">Click me</button>
        <main>
            <section>Section 1</section>
            <section>Section 2</section>
            <section>Section 3</section>
        </main>
        <footer></footer>
    </body>
    </html>
    """
    
    assert QualityValidator.check_html_syntax(html_content) == 100
    assert AccessibilityChecker.audit_accessibility(html_content) == 100
    assert SEOChecker.audit_seo(html_content) == 100
    assert PerformanceChecker.audit_performance(html_content) == 100
    assert UXChecker.audit_ux(html_content) == 100
    assert ComponentChecker.audit_components(html_content) == 100

def test_checkers_lower_scores():
    # Bad HTML
    bad_html = "<div>No header, footer, meta, canonical, landmarks, or sections"
    
    assert AccessibilityChecker.audit_accessibility(bad_html) < 100
    assert SEOChecker.audit_seo(bad_html) < 100
    assert UXChecker.audit_ux(bad_html) < 100
    assert ComponentChecker.audit_components(bad_html) < 100

# ---------------------------------------------------------
# Scoring & Certification Levels Tests
# ---------------------------------------------------------
def test_quality_scoring_weights():
    metrics = {
        "html": 100, "accessibility": 100, "performance": 100, "responsive": 100,
        "seo": 100, "ux": 100, "visual": 100, "component": 100
    }
    assert QualityScore.calculate_overall_score(metrics) == 100

    metrics_lower = {
        "html": 80, "accessibility": 80, "performance": 80, "responsive": 80,
        "seo": 80, "ux": 80, "visual": 80, "component": 80
    }
    assert QualityScore.calculate_overall_score(metrics_lower) == 80

def test_certification_engine():
    assert CertificationEngine.get_certification_level(98) == "Enterprise Certified"
    assert CertificationEngine.get_certification_level(92) == "Production Ready"
    assert CertificationEngine.get_certification_level(84) == "Client Presentation Ready"
    assert CertificationEngine.get_certification_level(75) == "Requires Minor Improvements"
    assert CertificationEngine.get_certification_level(65) == "Rejected"

# ---------------------------------------------------------
# Quality Analyzer Coordinator & SQLite Writes Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_quality_analyzer_db_upsert(tmp_path):
    analyzer = QualityAnalyzer()
    
    # Mock files
    html_file = str(tmp_path / "mock.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<html><title>Test</title><meta name='description' content='Desc'><link rel='canonical' href='c'><header></header><footer></footer><section></section></html>")

    mock_session = MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock query results (no existing record)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.quality_analyzer.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute analyzer
        res = await analyzer.analyze_quality(html_file, "mock.css", job_id=303)
        
        assert "quality_score" in res
        assert res["quality_score"] > 80
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeQuality)
        assert added_obj.job_id == 303
        assert added_obj.overall_score == res["quality_score"]

@pytest.mark.asyncio
async def test_quality_analyzer_deduplication(tmp_path):
    analyzer = QualityAnalyzer()
    html_file = str(tmp_path / "mock.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<html><title>Test</title><meta name='description' content='Desc'><link rel='canonical' href='c'><header></header><footer></footer><section></section></html>")

    mock_session = MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock existing record (deduplication update check)
    existing_record = PrototypeQuality(id=505, job_id=35, html_score=0, accessibility_score=0, performance_score=0, responsive_score=0, seo_score=0, ux_score=0, visual_score=0, component_score=0, overall_score=0, certification_level="Rejected")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.quality_analyzer.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await analyzer.analyze_quality(html_file, "mock.css", job_id=35)
        
        assert "quality_score" in res
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.overall_score == res["quality_score"] # updated
        assert existing_record.certification_level == res["certification_level"] # updated
