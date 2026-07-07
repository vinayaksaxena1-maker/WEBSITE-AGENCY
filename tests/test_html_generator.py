import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.prototype.tailwind_generator import TailwindGenerator
from agents.prototype.component_renderer import ComponentRenderer
from agents.prototype.token_injector import TokenInjector
from agents.prototype.accessibility_generator import AccessibilityGenerator
from agents.prototype.seo_generator import SEOGenerator
from agents.prototype.schema_generator import SchemaGenerator
from agents.prototype.asset_manager import AssetManager
from agents.prototype.build_optimizer import BuildOptimizer
from agents.prototype.html_validator import HTMLValidator
from agents.prototype.build_report import BuildReport
from agents.prototype.html_generator import HTMLGenerator
from agents.prototype.prototype_models import PrototypeBuild

# ---------------------------------------------------------
# Tailwind Generator & Variable Injection Tests
# ---------------------------------------------------------
def test_tailwind_generator_and_token_injection():
    theme = {
        "primary_color": "#FF0000",
        "secondary_color": "#00FF00",
        "accent_color": "#0000FF",
        "background_color": "#FFFFFF",
        "text_color": "#000000"
    }
    
    css = TailwindGenerator.get_root_styles(theme)
    assert "--primary: #FF0000;" in css
    assert "--secondary: #00FF00;" in css
    
    html = "<html><head></head><body></body></html>"
    injected = TokenInjector.inject_tokens(html, css)
    assert "<style>" in injected
    assert "--primary: #FF0000;" in injected

# ---------------------------------------------------------
# Component Renderer Mappings Tests
# ---------------------------------------------------------
def test_component_renderer_templates():
    structure = [
        {"type": "header"},
        {"type": "hero"}
    ]
    
    html = ComponentRenderer.render_layout(structure, "Super Title", "Super Body description details.")
    assert "<header" in html
    assert "Super Title" in html
    assert "Super Body description details." in html

# ---------------------------------------------------------
# Accessibility, SEO & Schema Injections Tests
# ---------------------------------------------------------
def test_seo_accessibility_and_schema_injectors():
    html = "<html><head></head><body><header><nav></nav></header><footer></footer></body></html>"
    
    # Accessibility
    acc = AccessibilityGenerator.enrich_accessibility(html)
    assert 'aria-label="Main Navigation"' in acc
    assert 'role="banner"' in acc
    
    # SEO
    metadata = {"heading_text": "SEO Title", "body_text": "SEO description meta tags block."}
    seo = SEOGenerator.inject_seo_tags(acc, metadata)
    assert "<title>SEO Title</title>" in seo
    assert 'content="SEO description meta tags block."' in seo
    
    # Schema JSON-LD
    schema = SchemaGenerator.inject_schema(seo, {"heading_text": "Org Name", "address": "123 Main St"})
    assert 'type="application/ld+json"' in schema
    assert '"name": "Org Name"' in schema

# ---------------------------------------------------------
# Asset Directories Security & Path Validation Tests
# ---------------------------------------------------------
def test_asset_manager_ensures_paths(tmp_path):
    target_dir = str(tmp_path / "prototype_out")
    AssetManager.ensure_directories(target_dir)
    
    assert os.path.exists(os.path.join(target_dir, "assets", "css"))
    assert os.path.exists(os.path.join(target_dir, "assets", "images"))

# ---------------------------------------------------------
# HTML Validator Syntax Tests
# ---------------------------------------------------------
def test_html_validator_syntax():
    valid_html = "<html><body><p>Valid tag closure</p></body></html>"
    assert HTMLValidator.validate_html_syntax(valid_html) is True

# ---------------------------------------------------------
# HTML Generator & SQLite Writes Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_html_generator_db_upsert(tmp_path):
    out_dir = str(tmp_path / "prototypes")
    generator = HTMLGenerator(output_dir=out_dir)
    components = [{"type": "hero", "variant": "split"}]
    theme = {"primary_color": "#1E3A8A"}

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
    
    with patch("agents.prototype.html_generator.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute HTML static generation and database storage
        res = await generator.generate(components, theme=theme, job_id=505)
        
        assert "html_path" in res
        assert "css_path" in res
        assert os.path.exists(res["html_path"])
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeBuild)
        assert added_obj.job_id == 505
        assert added_obj.seo_score == 95

@pytest.mark.asyncio
async def test_html_generator_deduplication(tmp_path):
    out_dir = str(tmp_path / "prototypes")
    generator = HTMLGenerator(output_dir=out_dir)
    components = [{"type": "hero", "variant": "split"}]
    theme = {"primary_color": "#1E3A8A"}

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
    existing_record = PrototypeBuild(id=707, job_id=90, build_version="0.1.0", html_size=0, seo_score=0)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.html_generator.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await generator.generate(components, theme=theme, job_id=90)
        
        assert "html_path" in res
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.seo_score == 95                  # updated
        assert existing_record.validation_status == "PASSED"     # updated
