import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from agents.prototype.component_library import COMPONENTS_LIBRARY
from agents.prototype.component_selector import ComponentSelector
from agents.prototype.component_tree import ComponentTree
from agents.prototype.variant_selector import VariantSelector
from agents.prototype.dependency_validator import DependencyValidator
from agents.prototype.component_validator import ComponentValidator
from agents.prototype.component_report import ComponentReport
from agents.prototype.component_engine import ComponentEngine
from agents.prototype.prototype_models import PrototypeComponent

# ---------------------------------------------------------
# Component Selector Mappings Tests
# ---------------------------------------------------------
def test_component_selector_mappings_and_fallbacks():
    sections = [
        {"type": "hero"},
        {"type": "faq"},
        {"type": "unknown_niche_section"}  # malformed/unknown
    ]
    
    selected = ComponentSelector.select_components(sections)
    assert len(selected) == 3
    assert selected[0]["name"] == "HeroComponent"
    assert selected[1]["name"] == "FAQComponent"
    # Fallback applied
    assert selected[2]["name"] == "CustomUnknown_niche_sectionSectionComponent"
    assert selected[0]["instance_id"] == "HeroComponent_0"

# ---------------------------------------------------------
# Tree Assembly Depth Safeguards Tests
# ---------------------------------------------------------
def test_component_tree_depth_safeguard():
    components = [
        {"instance_id": f"Comp_{i}", "name": f"Comp_{i}", "priority": "Medium", "order": i, "dependencies": []}
        for i in range(15)
    ]
    
    # Run with restrictive depth limit = 4
    tree = ComponentTree.build_tree(components, max_depth=4)
    # Root depth is 0. Children of root are depth 1. 
    # Children of children are depth 2.
    # Check max depth is bounded
    assert len(tree["children"]) > 0
    # Traverse children to verify none exceed max depth limit
    for child in tree["children"]:
        assert child["depth"] < 4

# ---------------------------------------------------------
# Dependency Cycles Tracing Tests
# ---------------------------------------------------------
def test_dependency_validator_safety_checks():
    components = [
        {"name": "HeroComponent", "dependencies": ["ButtonComponent"]},
        # ButtonComponent is missing in listing
    ]
    
    errors = DependencyValidator.validate_dependencies(components, max_cycles=5)
    assert len(errors) == 1
    assert "requires 'ButtonComponent'" in errors[0]

# ---------------------------------------------------------
# Component Engine & DB Transactions Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_component_engine_db_refresh():
    engine = ComponentEngine()
    layout = {"structure": [{"section": "hero"}, {"section": "faq"}]}
    theme = {"name": "tech-indigo-theme", "category": "Technology"}

    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.add = MagicMock()
    mock_session.flush = AsyncMock()
    
    mock_session.begin = MagicMock()
    mock_begin_context = MagicMock()
    mock_begin_context.__aenter__ = AsyncMock(return_value=None)
    mock_begin_context.__aexit__ = AsyncMock(return_value=False)
    mock_session.begin.return_value = mock_begin_context
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = MagicMock(return_value=False)
    
    with patch("agents.prototype.component_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute compilation and database writes
        res = await engine.assemble_components(layout, theme=theme, job_id=202)
        
        assert len(res) == 2
        assert res[0]["type"] == "hero"
        assert res[1]["type"] == "faq"
        
        # Check SQLite db write
        assert mock_session.add.called
        assert mock_session.execute.called  # called delete statement first
        
        added_objs = [call[0][0] for call in mock_session.add.call_args_list]
        assert len(added_objs) == 2
        assert isinstance(added_objs[0], PrototypeComponent)
        assert added_objs[0].job_id == 202
        assert added_objs[0].theme == "tech-indigo-theme"
        assert added_objs[1].component_name == "FAQComponent"
