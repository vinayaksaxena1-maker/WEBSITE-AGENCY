import os
import pytest
import time
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.prototype.preview_server import PreviewServer
from agents.prototype.render_validator import RenderValidator
from agents.prototype.device_renderer import DeviceRenderer
from agents.prototype.comparison_engine import ComparisonEngine
from agents.prototype.preview_capture import PreviewCapture
from agents.prototype.preview_metadata import PreviewMetadata
from agents.prototype.preview_report import PreviewReport
from agents.prototype.preview_generator import PreviewGenerator
from agents.prototype.prototype_models import PrototypePreview

# ---------------------------------------------------------
# Local Server socket lifecycle tests
# ---------------------------------------------------------
def test_preview_server_lifecycle(tmp_path):
    directory = str(tmp_path)
    server = PreviewServer(directory=directory, port=8991)
    
    # Start and stop cleanly
    server.start()
    time.sleep(0.2)
    assert server.server is not None
    
    server.stop()
    assert server.server is not None # reference remains but stopped

# ---------------------------------------------------------
# Viewports Resolutions and Captures Tests
# ---------------------------------------------------------
def test_device_renderer_resolutions():
    viewports = DeviceRenderer.get_viewports()
    assert "desktop" in viewports
    assert "mobile" in viewports
    assert viewports["desktop"] == (1440, 900)

def test_preview_capture_writes_image(tmp_path):
    out_file = str(tmp_path / "desktop.png")
    res = PreviewCapture.capture_screenshot("http://localhost:8080/index.html", out_file, 1024, 768)
    assert res is True
    assert os.path.exists(out_file)

# ---------------------------------------------------------
# Visual Comparison composite drawings tests
# ---------------------------------------------------------
def test_comparison_engine_composite(tmp_path):
    before = str(tmp_path / "before.png")
    after = str(tmp_path / "after.png")
    out = str(tmp_path / "comp.png")
    
    # Generate mock inputs
    PreviewCapture.capture_screenshot("url1", before, 100, 100)
    PreviewCapture.capture_screenshot("url2", after, 100, 100)
    
    success = ComparisonEngine.compile_comparison(before, after, out)
    assert success is True
    assert os.path.exists(out)

# ---------------------------------------------------------
# Metadata and Reports formatters tests
# ---------------------------------------------------------
def test_metadata_and_reports(tmp_path):
    img = str(tmp_path / "img.png")
    PreviewCapture.capture_screenshot("url", img, 50, 50)
    
    meta = PreviewMetadata.compile_metadata(img)
    assert meta["format"] == "PNG"
    assert meta["file_size"] > 0
    
    report = PreviewReport.generate_report(100, "PASSED", {"desktop": img})
    assert "Score: 100" in report
    assert "PASSED" in report

# ---------------------------------------------------------
# Preview Generator Coordinator & Database writes tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_preview_generator_db_upsert(tmp_path):
    out_dir = str(tmp_path / "previews")
    generator = PreviewGenerator(output_dir=out_dir)
    
    # Mock template file
    html_file = str(tmp_path / "index.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<html><body>Test</body></html>")

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
    
    with patch("agents.prototype.preview_generator.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute generator
        res_path = await generator.generate_preview(html_file, job_id=404)
        
        assert "mock_preview.png" in res_path
        assert os.path.exists(res_path)
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypePreview)
        assert added_obj.job_id == 404
        assert added_obj.preview_score == 100

@pytest.mark.asyncio
async def test_preview_generator_deduplication(tmp_path):
    out_dir = str(tmp_path / "previews")
    generator = PreviewGenerator(output_dir=out_dir)
    html_file = str(tmp_path / "index.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<html><body>Test</body></html>")

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
    existing_record = PrototypePreview(id=606, job_id=45, preview_version="0.1.0", preview_score=10)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.preview_generator.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res_path = await generator.generate_preview(html_file, job_id=45)
        
        assert "mock_preview.png" in res_path
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.preview_score == 100              # updated
        assert existing_record.status == "PASSED"                 # updated
