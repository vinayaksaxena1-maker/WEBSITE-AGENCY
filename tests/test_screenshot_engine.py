import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from datetime import datetime, timezone
from PIL import Image

# Modules under test
from agents.prototype.viewport_profiles import get_viewport_profile, list_viewport_profiles
from agents.prototype.scroll_engine import ScrollEngine
from agents.prototype.popup_handler import PopupHandler
from agents.prototype.image_optimizer import ImageOptimizer
from agents.prototype.metadata_generator import MetadataGenerator
from agents.prototype.screenshot_engine import ScreenshotEngine
from agents.prototype.prototype_models import PrototypeScreenshot, init_prototype_db
from agents.search.search_models import SearchLead
from database.database import db_manager

# ---------------------------------------------------------
# Viewport Profiles Tests
# ---------------------------------------------------------
def test_viewport_profiles():
    profiles = list_viewport_profiles()
    assert "desktop" in profiles
    assert "mobile" in profiles
    
    desktop = get_viewport_profile("desktop")
    assert desktop["width"] == 1920
    assert desktop["height"] == 1080

# ---------------------------------------------------------
# Scroll Engine Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_scroll_engine_execution():
    mock_page = AsyncMock()
    # Mock evaluate to check JS scroll queries trigger
    mock_page.evaluate = AsyncMock(return_value=None)
    
    engine = ScrollEngine(step_px=300, delay_ms=50, max_scrolls=20)
    await engine.scroll_to_bottom_and_restore(mock_page)
    
    assert mock_page.evaluate.call_count >= 2
    # Check it restored top
    mock_page.evaluate.assert_any_call("window.scrollTo(0, 0)")

# ---------------------------------------------------------
# Popup Handler Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_popup_handler_dismiss():
    mock_page = AsyncMock()
    mock_element = AsyncMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    
    # Wait for selector returns mock element on first call, raises error for others
    mock_page.wait_for_selector = AsyncMock(side_effect=[mock_element] + [Exception("Not found")] * 100)
    
    handler = PopupHandler()
    await handler.dismiss_popups(mock_page)
    
    assert mock_element.click.called

# ---------------------------------------------------------
# Image Optimizer Tests
# ---------------------------------------------------------
def test_image_optimizer_lossless_compression(tmp_path):
    input_file = os.path.join(tmp_path, "test.png")
    
    # Create a non-optimized image (Grayscale mode 'L')
    img = Image.new("L", (800, 600), color=128)
    img.save(input_file, format="PNG")
    
    initial_size = os.path.getsize(input_file)
    
    # Compress it
    optimized_path = ImageOptimizer.compress_png(input_file, max_size_kb=500)
    assert optimized_path == input_file
    
    # Validate it's still a valid image and format is PNG
    with Image.open(optimized_path) as opt_img:
        assert opt_img.mode == "RGB"  # Converted from L to RGB
        assert opt_img.format == "PNG"

# ---------------------------------------------------------
# Metadata Generator Tests
# ---------------------------------------------------------
def test_metadata_compilation(tmp_path):
    dummy_file = os.path.join(tmp_path, "dummy.png")
    with open(dummy_file, "w") as f:
        f.write("mock_content")
        
    meta = MetadataGenerator.compile_metadata(
        viewport_name="desktop",
        width=1920,
        height=1080,
        browser="chromium",
        duration=1.234,
        file_path=dummy_file
    )
    
    assert meta["viewport_profile"] == "desktop"
    assert meta["width"] == 1920
    assert meta["capture_duration_seconds"] == 1.234
    assert meta["file_size_bytes"] == len("mock_content")
    assert "timestamp_utc" in meta

# ---------------------------------------------------------
# Screenshot Engine DB Updates & Fallback Test
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_screenshot_engine_fallback_and_db_writes(tmp_path):
    # Output directory in tmp test path
    out_dir = os.path.join(tmp_path, "screenshots")
    engine = ScreenshotEngine(output_dir=out_dir)
    
    # Mock database context managers and sessions
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
    
    # Mock query results (no existing screenshot)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.screenshot_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Run capture with mock fallback
        res = await engine.capture("https://fallback-test.com", job_id=45)
        
        assert res["success"] is True
        assert res["page_width"] == 1920
        assert res["page_height"] == 3000
        assert "desktop" in res["metadata"]
        
        # Verify filesystem creations
        assert os.path.exists(res["desktop_path"])
        assert os.path.exists(res["fullpage_path"])
        
        # Verify db mock calls
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeScreenshot)
        assert added_obj.job_id == 45
        assert added_obj.browser == "chromium"

@pytest.mark.asyncio
async def test_screenshot_engine_deduplication(tmp_path):
    out_dir = os.path.join(tmp_path, "screenshots")
    engine = ScreenshotEngine(output_dir=out_dir)
    
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
    
    # Mock existing screenshot (deduplication update check)
    existing_screenshot = PrototypeScreenshot(id=77, job_id=50, browser="firefox", status="PENDING")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_screenshot
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.screenshot_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await engine.capture("https://dedup-test.com", job_id=50)
        
        assert res["success"] is True
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_screenshot.browser == "chromium"  # updated
        assert existing_screenshot.status == "CAPTURED"    # updated
