import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from agents.prototype.export_validator import ExportValidator
from agents.prototype.package_builder import PackageBuilder
from agents.prototype.manifest_generator import ManifestGenerator
from agents.prototype.version_manager import VersionManager
from agents.prototype.checksum_generator import ChecksumGenerator
from agents.prototype.asset_packager import AssetPackager
from agents.prototype.integrity_checker import IntegrityChecker
from agents.prototype.export_report import ExportReport
from agents.prototype.export_engine import ExportEngine
from agents.prototype.prototype_models import PrototypeExport

# ---------------------------------------------------------
# Validator & Version manager Tests
# ---------------------------------------------------------
def test_export_validator_credentials():
    clean_html = "<html><body><h1>Welcome</h1></body></html>"
    dirty_html = "<html><body><h1>Welcome</h1><script>const apiKey = 'abcde12345fghij67890';</script></body></html>"
    
    assert ExportValidator.scan_for_credentials(clean_html) is True
    assert ExportValidator.scan_for_credentials(dirty_html) is False

def test_version_increments():
    assert VersionManager.get_next_version("1.0.0", "patch") == "1.0.1"
    assert VersionManager.get_next_version("1.0.0", "minor") == "1.1.0"
    assert VersionManager.get_next_version("1.0.0", "major") == "2.0.0"
    assert VersionManager.get_next_version("bad_ver") == "1.0.0"

# ---------------------------------------------------------
# Manifest & Checksums Generators Tests
# ---------------------------------------------------------
def test_manifest_and_checksums(tmp_path):
    manifest_path = str(tmp_path / "manifest.json")
    meta = {"version": "1.2.3"}
    success = ManifestGenerator.generate_manifest(meta, manifest_path)
    assert success is True
    assert os.path.exists(manifest_path)
    
    chk = ChecksumGenerator.calculate_sha256(manifest_path)
    assert len(chk) == 64 # SHA-256 hex digest length

# ---------------------------------------------------------
# Asset Packager and Package Builder Tests
# ---------------------------------------------------------
def test_asset_packager_and_zipping(tmp_path):
    html = str(tmp_path / "index.html")
    css = str(tmp_path / "mock.css")
    with open(html, "w") as f: f.write("HTML")
    with open(css, "w") as f: f.write("CSS")
    
    dest_dir = str(tmp_path / "out_dist")
    AssetPackager.collect_assets(html, css, dest_dir)
    assert os.path.exists(os.path.join(dest_dir, "index.html"))
    
    zip_path = str(tmp_path / "output.zip")
    pkg_size = PackageBuilder.create_zip(dest_dir, zip_path)
    assert pkg_size > 0
    assert os.path.exists(zip_path)
    
    assert IntegrityChecker.verify_zip_integrity(zip_path) is True

# ---------------------------------------------------------
# Export Engine Coordinator & Database writes tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_export_engine_db_upsert(tmp_path):
    out_dir = str(tmp_path / "exports")
    engine = ExportEngine(export_dir=out_dir)
    
    # Mock template files
    html = str(tmp_path / "index.html")
    css = str(tmp_path / "mock.css")
    with open(html, "w") as f: f.write("<html><body>Clean</body></html>")
    with open(css, "w") as f: f.write("body { color: blue; }")

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
    
    with patch("agents.prototype.export_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute export engine package compilation
        res = await engine.export_prototype(html, css, theme_name="schools-modern", job_id=202)
        
        assert res["success"] is True
        assert "zip_path" in res
        assert os.path.exists(res["zip_path"])
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeExport)
        assert added_obj.job_id == 202
        assert added_obj.package_size == res["package_size"]

@pytest.mark.asyncio
async def test_export_engine_deduplication(tmp_path):
    out_dir = str(tmp_path / "exports")
    engine = ExportEngine(export_dir=out_dir)
    html = str(tmp_path / "index.html")
    css = str(tmp_path / "mock.css")
    with open(html, "w") as f: f.write("<html><body>Clean</body></html>")
    with open(css, "w") as f: f.write("body { color: blue; }")

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
    existing_record = PrototypeExport(id=909, job_id=45, export_version="0.1.0", package_name="old.zip", package_size=0, checksum="abc")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.export_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await engine.export_prototype(html, css, theme_name="schools-modern", job_id=45)
        
        assert res["success"] is True
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.package_name == "prototype_job_45.zip" # updated
        assert existing_record.package_size == res["package_size"]      # updated
