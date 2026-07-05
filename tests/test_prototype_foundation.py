import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from datetime import datetime, timezone
from sqlalchemy import select

# Import modules under test
from agents.prototype.prototype_models import (
    PrototypeJob, PrototypeResult, PrototypeReport, PrototypeAsset, init_prototype_db
)
from agents.prototype.browser_engine import BrowserEngine
from agents.prototype.screenshot_engine import ScreenshotEngine
from agents.prototype.dom_analyzer import DOMAnalyzer
from agents.prototype.visual_analyzer import VisualAnalyzer
from agents.prototype.theme_engine import ThemeEngine
from agents.prototype.layout_engine import LayoutEngine
from agents.prototype.component_engine import ComponentEngine
from agents.prototype.responsive_engine import ResponsiveEngine
from agents.prototype.html_generator import HTMLGenerator
from agents.prototype.preview_generator import PreviewGenerator
from agents.prototype.quality_analyzer import QualityAnalyzer
from agents.prototype.prototype_pipeline import PrototypePipeline
from agents.prototype.prototype_agent import PrototypeAgent
from agents.search.search_models import SearchLead
from database.database import db_manager

# ---------------------------------------------------------
# Individual Engines Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_browser_engine():
    engine = BrowserEngine()
    launched = await engine.launch()
    assert launched is True
    page_content = await engine.get_page("https://example.com")
    assert "Mock Content" in page_content
    await engine.close()

@pytest.mark.asyncio
async def test_screenshot_engine():
    engine = ScreenshotEngine(output_dir="tmp/assets")
    screenshots = await engine.capture("https://example.com")
    assert "desktop" in screenshots
    assert "mobile" in screenshots
    assert screenshots["desktop"] == "tmp/assets/desktop_mock.png"

@pytest.mark.asyncio
async def test_dom_analyzer():
    analyzer = DOMAnalyzer()
    res = await analyzer.analyze("<html></html>")
    assert "Hero" in res["sections"]
    assert len(res["ctas"]) > 0

@pytest.mark.asyncio
async def test_visual_analyzer():
    analyzer = VisualAnalyzer()
    res = await analyzer.analyze_visuals({"desktop": "mock.png"})
    assert res["primary_color"] == "#1E3A8A"
    assert res["visual_score"] == 75

@pytest.mark.asyncio
async def test_theme_engine():
    engine = ThemeEngine()
    theme = await engine.select_theme("clinic", {"primary_color": "#FF0000"})
    assert theme["colors"]["primary"] == "#FF0000"
    assert theme["colors"]["accent"] == "#F59E0B"

@pytest.mark.asyncio
async def test_layout_engine():
    engine = LayoutEngine()
    layout = await engine.create_layout_grid(["Hero", "About"], {"name": "my-theme"})
    assert layout["layout_type"] == "one-page-app"
    assert layout["theme_name"] == "my-theme"

@pytest.mark.asyncio
async def test_component_engine():
    engine = ComponentEngine()
    comps = await engine.assemble_components({"structure": [{"section": "hero", "layout": "split"}]})
    assert len(comps) == 1
    assert comps[0]["type"] == "hero"

@pytest.mark.asyncio
async def test_responsive_engine():
    engine = ResponsiveEngine()
    comps = await engine.make_responsive([{"type": "hero", "classes": "bg-red-500"}])
    assert "max-w-7xl" in comps[0]["classes"]

@pytest.mark.asyncio
async def test_html_generator():
    gen = HTMLGenerator(output_dir="tmp")
    files = await gen.generate([{"type": "hero"}], {"name": "theme"})
    assert files["html_path"] == "tmp/mock_prototype.html"

@pytest.mark.asyncio
async def test_preview_generator():
    gen = PreviewGenerator(output_dir="tmp/previews")
    preview = await gen.generate_preview("tmp/mock_prototype.html")
    assert preview == "tmp/previews/mock_preview.png"

@pytest.mark.asyncio
async def test_quality_analyzer():
    analyzer = QualityAnalyzer()
    res = await analyzer.analyze_quality("mock.html", "mock.css")
    assert res["quality_score"] == 96
    assert len(res["improvements"]) > 0

# ---------------------------------------------------------
# Pipeline Integration Test
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_prototype_pipeline_integration():
    pipeline = PrototypePipeline()
    res = await pipeline.execute_pipeline("https://testsite.com", "schools")
    assert res["success"] is True
    assert res["quality_score"] == 96
    assert res["theme_name"] == "schools-modern-theme"
    assert len(res["assets"]) == 5

# ---------------------------------------------------------
# Agent Integration Test
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_prototype_agent_execution_success():
    # Mocking Database Session contexts
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock lead fetch
    lead = SearchLead(id=12, domain="testsite.com", source="DDG", niche="schools", status="VALIDATED")
    mock_result_lead = MagicMock()
    mock_result_lead.scalars.return_value.first.return_value = lead
    
    # Mock no existing job (first run)
    mock_result_job = MagicMock()
    mock_result_job.scalars.return_value.first.return_value = None
    
    # Mock existing result and report for upsert branches
    mock_result_res = MagicMock()
    mock_result_res.scalars.return_value.first.return_value = None
    mock_result_rep = MagicMock()
    mock_result_rep.scalars.return_value.first.return_value = None
    mock_result_assets = MagicMock()
    mock_result_assets.scalars.return_value.all.return_value = []
    
    # Side effects for session.execute queries
    mock_session.execute.side_effect = [
        mock_result_lead,    # Step 1: verify lead existence
        mock_result_job,     # Step 2: verify job exists
        mock_result_job,     # Step 4: re-fetch job
        mock_result_lead,    # Step 4: re-fetch lead
        mock_result_res,     # Step 4: check existing result
        mock_result_rep,     # Step 4: check existing report
        mock_result_assets,  # Step 4: fetch existing assets
    ]
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = AsyncMock()
    
    with patch("agents.prototype.prototype_agent.db_manager") as mock_db_mgr, \
         patch("agents.prototype.prototype_agent.redis_manager", mock_redis), \
         patch("agents.prototype.prototype_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = PrototypeAgent()
        payload = await agent.execute_for_lead(12, "https://testsite.com")
        
        # Verify status transitions & DB additions
        assert payload["success"] is True
        assert lead.status == "PROTOTYPED"
        assert mock_redis.push_to_queue.called
        mock_redis.push_to_queue.assert_called_with("email_queue", "https://testsite.com")
        
        assert mock_event_bus.publish.called
        mock_event_bus.publish.assert_called_with("prototype_generated", ANY)

@pytest.mark.asyncio
async def test_prototype_agent_execution_deduplication():
    # Mock lead fetch
    lead = SearchLead(id=15, domain="testsite.com", source="DDG", niche="dentists", status="VALIDATED")
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock existing job (deduplication check)
    existing_job = PrototypeJob(id=99, lead_id=15, website_url="https://testsite.com", status="PENDING")
    mock_result_job = MagicMock()
    mock_result_job.scalars.return_value.first.return_value = existing_job
    
    mock_result_lead = MagicMock()
    mock_result_lead.scalars.return_value.first.return_value = lead
    
    mock_result_res = MagicMock()
    mock_result_res.scalars.return_value.first.return_value = PrototypeResult(id=1, job_id=99)
    mock_result_rep = MagicMock()
    mock_result_rep.scalars.return_value.first.return_value = PrototypeReport(id=2, job_id=99)
    mock_result_assets = MagicMock()
    mock_result_assets.scalars.return_value.all.return_value = [PrototypeAsset(id=3, job_id=99)]
    
    mock_session.execute.side_effect = [
        mock_result_lead,    # Step 1: verify lead
        mock_result_job,     # Step 2: verify job
        mock_result_job,     # Step 4: re-fetch job
        mock_result_lead,    # Step 4: re-fetch lead
        mock_result_res,     # Step 4: check existing result
        mock_result_rep,     # Step 4: check existing report
        mock_result_assets,  # Step 4: fetch existing assets
    ]
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    mock_redis = AsyncMock()
    mock_event_bus = AsyncMock()
    
    with patch("agents.prototype.prototype_agent.db_manager") as mock_db_mgr, \
         patch("agents.prototype.prototype_agent.redis_manager", mock_redis), \
         patch("agents.prototype.prototype_agent.event_bus", mock_event_bus):
         
        mock_db_mgr.session_factory = mock_session_factory
        
        agent = PrototypeAgent()
        payload = await agent.execute_for_lead(15, "https://testsite.com")
        
        assert payload["success"] is True
        assert existing_job.status == "COMPLETED"
        assert lead.status == "PROTOTYPED"
