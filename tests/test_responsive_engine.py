import pytest
import json
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.prototype.breakpoint_manager import BreakpointManager
from agents.prototype.responsive_rules import ResponsiveRules
from agents.prototype.grid_adapter import GridAdapter
from agents.prototype.container_adapter import ContainerAdapter
from agents.prototype.component_adapter import ComponentAdapter
from agents.prototype.typography_scaler import TypographyScaler
from agents.prototype.spacing_scaler import SpacingScaler
from agents.prototype.navigation_adapter import NavigationAdapter
from agents.prototype.responsive_validator import ResponsiveValidator
from agents.prototype.responsive_report import ResponsiveReport
from agents.prototype.responsive_engine import ResponsiveEngine
from agents.prototype.prototype_models import PrototypeResponsive

# ---------------------------------------------------------
# Breakpoints, rules and grid collapse unit tests
# ---------------------------------------------------------
def test_breakpoint_manager():
    bps = BreakpointManager.get_breakpoints()
    assert "Desktop XL" in bps
    assert "Mobile" in bps
    assert bps["Desktop XL"]["grid_columns"] == 12
    assert bps["Mobile"]["grid_columns"] == 2

def test_responsive_rules_widths():
    widths = ResponsiveRules.get_container_widths()
    assert "Desktop XL" in widths
    assert "max-w-7xl" in widths["Desktop XL"]
    assert "w-full" in widths["Mobile"]

def test_grid_adapter_collapsing():
    # 12 columns should collapse to 1 on Mobile, 2 on Mobile Large, 6 on Tablet
    assert GridAdapter.adapt_grid(12, "Mobile") == 1
    assert GridAdapter.adapt_grid(12, "Small Mobile") == 1
    assert GridAdapter.adapt_grid(12, "Mobile Large") == 2
    assert GridAdapter.adapt_grid(12, "Tablet") == 6
    assert GridAdapter.adapt_grid(12, "Desktop") == 12

def test_container_and_component_adapters():
    assert ContainerAdapter.get_padding_rules("Mobile") == "px-4 py-8"
    assert ContainerAdapter.get_padding_rules("Desktop") == "px-8 py-16"
    
    assert "col" in ComponentAdapter.adapt_card_layout("Mobile")
    assert "cols-3" in ComponentAdapter.adapt_card_layout("Desktop")

# ---------------------------------------------------------
# Scaling (Typography, Spacings) & Navigation tests
# ---------------------------------------------------------
def test_typography_and_spacing_scalers():
    # Font size 32 should scale down by 0.7 on Mobile (32 * 0.7 = 22)
    assert TypographyScaler.get_scaled_font(32, "Mobile") == 22
    assert TypographyScaler.get_scaled_font(32, "Desktop") == 32
    
    # Gap size 16 should scale down by 0.5 on Mobile (16 * 0.5 = 8)
    assert SpacingScaler.get_scaled_gap(16, "Mobile") == 8
    assert SpacingScaler.get_scaled_gap(16, "Desktop") == 16

def test_navigation_drawer_switches():
    assert NavigationAdapter.get_navigation_style("Desktop") == "horizontal-navbar"
    assert NavigationAdapter.get_navigation_style("Mobile") == "hamburger-drawer"

# ---------------------------------------------------------
# Responsive Engine Pipeline & SQLite Database writes tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_responsive_engine_db_upsert():
    engine = ResponsiveEngine()
    components = [{"type": "hero", "classes": ""}]

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
    
    with patch("agents.prototype.responsive_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute adaptation rules engine compilation
        res = await engine.make_responsive(components, job_id=606)
        
        assert len(res) == 1
        assert "responsive_blueprint" in res[0]
        assert res[0]["responsive_score"] == 100
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeResponsive)
        assert added_obj.job_id == 606
        assert added_obj.responsive_score == 100

@pytest.mark.asyncio
async def test_responsive_engine_deduplication():
    engine = ResponsiveEngine()
    components = [{"type": "hero"}]

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
    existing_record = PrototypeResponsive(id=808, job_id=88, breakpoint_profile="{}", device_support="[]", responsive_score=50, validation_status="FAILED")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.responsive_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await engine.make_responsive(components, job_id=88)
        
        assert len(res) == 1
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.responsive_score == 100          # updated
        assert existing_record.validation_status == "PASSED"     # updated
