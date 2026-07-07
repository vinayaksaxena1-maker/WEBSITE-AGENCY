import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from bs4 import BeautifulSoup
from agents.prototype.color_normalizer import ColorNormalizer
from agents.prototype.style_extractor import StyleExtractor
from agents.prototype.visual_score_calculator import VisualScoreCalculator
from agents.prototype.visual_analyzer import VisualAnalyzer
from agents.prototype.prototype_models import PrototypeVisualAnalysis

# ---------------------------------------------------------
# Color Normalization Tests
# ---------------------------------------------------------
def test_color_normalizer_conversions():
    # Hex Expanded
    assert ColorNormalizer.normalize_color("#1e3") == "#11EE33"
    # Hex Standard
    assert ColorNormalizer.normalize_color("#FF00FF") == "#FF00FF"
    # Named Colors
    assert ColorNormalizer.normalize_color("red") == "#FF0000"
    # RGB Conversion
    assert ColorNormalizer.normalize_color("rgb(30, 58, 138)") == "#1E3A8A"
    # RGBA Conversion (alpha dropped)
    assert ColorNormalizer.normalize_color("rgba(30, 58, 138, 0.4)") == "#1E3A8A"
    # HSL Conversion
    assert ColorNormalizer.normalize_color("hsl(240, 100%, 50%)") == "#0000FF"
    # Fallback Invalid Color
    assert ColorNormalizer.normalize_color("invalid-color-name", fallback="#CCCCCC") == "#CCCCCC"

# ---------------------------------------------------------
# Style Extractor Tests
# ---------------------------------------------------------
def test_style_extractor_frequency_resolution():
    raw_html = """
    <html>
      <body style="background-color: rgb(255,255,255); color: #333333; font-family: 'Open Sans', sans-serif;">
        <button style="color: rgb(30,58,138);">Click 1</button>
        <a href="#" style="color: rgb(30,58,138);">Link 2</a>
        <a href="#" style="color: #F59E0B;">Link 3</a>
      </body>
    </html>
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    colors, font_family = StyleExtractor.extract_styles(soup)
    
    assert colors["background_color"] == "#FFFFFF"
    assert colors["text_color"] == "#333333"
    assert colors["primary_color"] == "#1E3A8A"       # Count = 2
    assert colors["secondary_color"] == "#F59E0B"     # Count = 1
    assert font_family == "Open Sans"

# ---------------------------------------------------------
# Visual Score Calculator Tests
# ---------------------------------------------------------
def test_visual_score_rating():
    raw_html = """
    <html>
      <body>
        <div></div><div></div><div></div>
        <img src="img1.png" /><img src="img2.png" />
        <button>Btn</button>
      </body>
    </html>
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    # Base 50 + image count + button count
    score = VisualScoreCalculator.calculate_score(soup, colors_count=3)
    assert 50 <= score <= 100

# ---------------------------------------------------------
# Visual Analyzer DB Operations Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_visual_analyzer_pipeline_and_db_upsert():
    html_content = "<body style='background-color: #FFFFFF; color: #000000;'><button style='color: #1E3A8A;'>Submit</button></body>"
    analyzer = VisualAnalyzer()

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
    
    # Mock query results (no existing record)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.visual_analyzer.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute analysis and database storage
        res = await analyzer.analyze_visuals(screenshots={}, html_content=html_content, job_id=95)
        
        assert res["success"] is True
        assert res["primary_color"] == "#1E3A8A"
        assert res["background_color"] == "#FFFFFF"
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeVisualAnalysis)
        assert added_obj.job_id == 95
        assert added_obj.primary_color == "#1E3A8A"

@pytest.mark.asyncio
async def test_visual_analyzer_deduplication():
    html_content = "<body style='background-color: #FFFFFF; color: #000000;'><button style='color: #1E3A8A;'>Submit</button></body>"
    analyzer = VisualAnalyzer()

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
    
    # Mock existing record (deduplication update check)
    existing_record = PrototypeVisualAnalysis(id=101, job_id=45, primary_color="#000000", status="PENDING")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.visual_analyzer.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await analyzer.analyze_visuals(screenshots={}, html_content=html_content, job_id=45)
        
        assert res["success"] is True
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.primary_color == "#1E3A8A"  # updated
        assert existing_record.status == "ANALYZED"          # updated
