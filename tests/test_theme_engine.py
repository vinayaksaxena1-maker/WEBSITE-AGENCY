import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.prototype.theme_library import get_theme_preset
from agents.prototype.theme_selector import ThemeSelector
from agents.prototype.theme_tokens import ThemeTokens
from agents.prototype.theme_validator import ThemeValidator
from agents.prototype.theme_report import ThemeReport
from agents.prototype.theme_engine import ThemeEngine
from agents.prototype.prototype_models import PrototypeTheme

# ---------------------------------------------------------
# Niche Mapping Library Tests
# ---------------------------------------------------------
def test_theme_library_niche_fuzzy_matches():
    # Clinic matches medical preset
    med_preset = get_theme_preset("Dental Clinic")
    assert med_preset["category"] == "Medical"
    
    # Gym matches fitness preset
    fit_preset = get_theme_preset("Crossfit Gym")
    assert fit_preset["category"] == "Bold Marketing"
    
    # Random niche fallback
    default_preset = get_theme_preset("Bakery Store")
    assert default_preset["category"] == "Modern Business"

# ---------------------------------------------------------
# Theme Selector Tests
# ---------------------------------------------------------
def test_theme_selector_merging():
    # Clinic category with custom visual primary color
    visuals = {"primary_color": "#FF5500", "secondary_color": "#00FF00"}
    theme = ThemeSelector.select_theme("clinic", visuals)
    
    assert theme["colors"]["primary"] == "#FF5500"  # Merged
    assert theme["colors"]["secondary"] == "#00FF00"  # Merged
    assert theme["colors"]["accent"] == "#F59E0B"  # Preserved preset accent

# ---------------------------------------------------------
# Spacing & Radii Token Generation Tests
# ---------------------------------------------------------
def test_theme_tokens_generation():
    theme = {
        "name": "Luxury Fashion Theme",
        "category": "Premium Luxury",
        "colors": {},
        "typography": {}
    }
    
    tokens = ThemeTokens.compile_tokens(theme)
    assert "spacing" in tokens
    assert "typography" in tokens
    # Premium luxury category maps to sharp/4px buttons
    assert tokens["radius"]["button"] == "4px"

# ---------------------------------------------------------
# WCAG Contrast & Luminance Math Tests
# ---------------------------------------------------------
def test_wcag_luminance_and_contrast_ratio():
    # Pure White relative luminance = 1.0
    white_lum = ThemeValidator.calculate_relative_luminance("#FFFFFF")
    assert white_lum == 1.0
    
    # Pure Black relative luminance = 0.0
    black_lum = ThemeValidator.calculate_relative_luminance("#000000")
    assert black_lum == 0.0
    
    # Contrast ratio of white vs black = 21.0
    ratio = ThemeValidator.get_contrast_ratio("#FFFFFF", "#000000")
    assert ratio == 21.0
    
    # Contrast ratio of white vs white = 1.0
    ratio_same = ThemeValidator.get_contrast_ratio("#FFFFFF", "#FFFFFF")
    assert ratio_same == 1.0

# ---------------------------------------------------------
# Theme Engine Pipeline & SQLite Writes Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_theme_engine_db_upsert():
    engine = ThemeEngine()
    visuals = {"primary_color": "#EA580C"}
    
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
    
    with patch("agents.prototype.theme_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute theme selection and database storage
        res = await engine.select_theme("fitness", visuals, job_id=110)
        
        assert res["name"] == "fitness-modern-theme"
        assert res["colors"]["primary"] == "#EA580C"
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeTheme)
        assert added_obj.job_id == 110
        assert added_obj.industry == "fitness"
        assert added_obj.theme_score > 50

@pytest.mark.asyncio
async def test_theme_engine_deduplication():
    engine = ThemeEngine()
    visuals = {"primary_color": "#DC2626"}
    
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
    existing_record = PrototypeTheme(id=303, job_id=60, theme_name="old-theme", primary_color="#000000")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = MagicMock(return_value=False)
    
    with patch("agents.prototype.theme_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await engine.select_theme("restaurant", visuals, job_id=60)
        
        assert res["name"] == "restaurant-modern-theme"
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.theme_name == "restaurant-modern-theme"  # updated
        assert existing_record.primary_color == "#DC2626"                # updated
