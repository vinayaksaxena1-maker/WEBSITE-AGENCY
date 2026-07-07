import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.prototype.layout_selector import LayoutSelector
from agents.prototype.grid_builder import GridBuilder
from agents.prototype.sequence_sorter import SequenceSorter
from agents.prototype.spacing_rules import SpacingRules
from agents.prototype.layout_validator import LayoutValidator
from agents.prototype.layout_engine import LayoutEngine
from agents.prototype.prototype_models import PrototypeTemplate

# ---------------------------------------------------------
# Layout Selector Tests
# ---------------------------------------------------------
def test_layout_selector_niche_mapping():
    assert LayoutSelector.select_layout_type("Creative Portfolio") == "portfolio-layout"
    assert LayoutSelector.select_layout_type("E-Commerce Shop") == "e-commerce-grid"
    assert LayoutSelector.select_layout_type("Medical Clinic") == "one-page-app"

# ---------------------------------------------------------
# Tailwind Columns Translation Matrix Tests
# ---------------------------------------------------------
def test_grid_builder_classes_mapping():
    assert "col-span-12" in GridBuilder.get_tailwind_classes(1)
    assert "lg:col-span-6" in GridBuilder.get_tailwind_classes(2)
    assert "lg:col-span-4" in GridBuilder.get_tailwind_classes(3)
    assert "lg:col-span-3" in GridBuilder.get_tailwind_classes(4)

# ---------------------------------------------------------
# Section Sequencing Reordering Tests
# ---------------------------------------------------------
def test_sequence_sorter_flow():
    sections = [
        {"section": "faq"},
        {"section": "hero"},
        {"section": "footer"},
        {"section": "header"},
        {"section": "services"}
    ]
    
    sorted_flow = SequenceSorter.sort_sequence(sections)
    assert sorted_flow[0]["section"] == "header"
    assert sorted_flow[1]["section"] == "hero"
    assert sorted_flow[2]["section"] == "services"
    assert sorted_flow[3]["section"] == "faq"
    assert sorted_flow[4]["section"] == "footer"

# ---------------------------------------------------------
# Auto-Injection Recovery Protection Tests
# ---------------------------------------------------------
def test_layout_validator_auto_injections():
    # Input has no header and footer
    sections = [{"section": "hero"}, {"section": "contact"}]
    
    validated = LayoutValidator.validate_and_repair(sections)
    assert len(validated) == 4
    assert validated[0]["section"] == "header"
    assert validated[-1]["section"] == "footer"

# ---------------------------------------------------------
# Layout Engine & SQLite Writes Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_layout_engine_db_upsert():
    engine = LayoutEngine()
    sections = ["hero", "services", "contact"]
    theme = {"name": "medical-preset-theme", "category": "Medical"}

    mock_session = AsyncMock()
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
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = MagicMock(return_value=False)
    
    with patch("agents.prototype.layout_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute grid layout creation and database storage
        res = await engine.create_layout_grid(sections, theme=theme, job_id=305)
        
        assert res["layout_type"] == "one-page-app"
        assert res["columns_count"] == 3  # due to services section presence
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeTemplate)
        assert added_obj.job_id == 305
        assert added_obj.columns_count == 3
        assert "header" in added_obj.section_sequence

@pytest.mark.asyncio
async def test_layout_engine_deduplication():
    engine = LayoutEngine()
    sections = ["hero", "contact"]
    theme = {"name": "agency-theme", "category": "Creative Agency"}

    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    # Mock existing record (deduplication update check)
    existing_record = PrototypeTemplate(id=505, job_id=88, layout_type="old-layout", columns_count=1)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute.return_value = mock_result
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = MagicMock(return_value=False)
    
    with patch("agents.prototype.layout_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await engine.create_layout_grid(sections, theme=theme, job_id=88)
        
        assert res["layout_type"] == "one-page-app"
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.layout_type == "one-page-app"  # updated
        assert "header" in existing_record.section_sequence    # updated
