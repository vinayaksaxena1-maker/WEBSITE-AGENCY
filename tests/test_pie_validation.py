import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from agents.prototype.integration_validator import IntegrationValidator
from agents.prototype.pipeline_validator import PipelineValidator
from agents.prototype.production_checker import ProductionChecker
from agents.prototype.release_manager import ReleaseManager
from agents.prototype.phase_lock import PhaseLock
from agents.prototype.certification_generator import CertificationGenerator
from agents.prototype.final_report import FinalReport
from agents.prototype.pie_validation_engine import PIEValidationEngine
from agents.prototype.validation_models import PrototypeRelease

# ---------------------------------------------------------
# Integration & Pipeline validators unit tests
# ---------------------------------------------------------
def test_validators():
    assert IntegrationValidator.check_modules_communication() is True
    assert PipelineValidator.verify_pipeline_stages() is True
    assert ProductionChecker.run_checklist_checks() is True
    assert PhaseLock.execute_phase_lock() is True

def test_release_decisions():
    status_pass, ready_pass = ReleaseManager.get_release_decision(94)
    status_fail, ready_fail = ReleaseManager.get_release_decision(65)
    
    assert status_pass == "PASS" and ready_pass is True
    assert status_fail == "FAIL" and ready_fail is False

# ---------------------------------------------------------
# Certification levels unit tests
# ---------------------------------------------------------
def test_certification_generator():
    c_a_plus = CertificationGenerator.generate_pie_certificate(98)
    c_a = CertificationGenerator.generate_pie_certificate(92)
    c_b = CertificationGenerator.generate_pie_certificate(85)
    
    assert c_a_plus["quality_grade"] == "Level A+"
    assert c_a["quality_grade"] == "Level A"
    assert c_b["quality_grade"] == "Level B"
    assert "certificate_id" in c_a_plus

# ---------------------------------------------------------
# Validation Engine Coordinator & Database Writes Tests
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_validation_engine_db_upsert():
    engine = PIEValidationEngine()

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
    
    with patch("agents.prototype.pie_validation_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        # Execute validation engine
        res = await engine.execute_final_validation(overall_score=98, version="1.0.0")
        
        assert res["success"] is True
        assert res["release_status"] == "PASS"
        assert res["production_ready"] is True
        
        # Verify db insert called
        assert mock_session.add.called
        added_obj = mock_session.add.call_args[0][0]
        assert isinstance(added_obj, PrototypeRelease)
        assert added_obj.release_version == "1.0.0"
        assert added_obj.certification_level == "Level A+"

@pytest.mark.asyncio
async def test_validation_engine_deduplication():
    engine = PIEValidationEngine()

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
    existing_record = PrototypeRelease(id=101, release_version="2.0.0", architecture_version="EDK-V7", certification_level="Level B", overall_score=85, production_ready=True, release_status="PASS")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    mock_session_factory = MagicMock()
    mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=False)
    
    with patch("agents.prototype.pie_validation_engine.db_manager") as mock_db_mgr:
        mock_db_mgr.session_factory = mock_session_factory
        
        res = await engine.execute_final_validation(overall_score=97, version="2.0.0")
        
        assert res["success"] is True
        # Verify it updated existing instead of creating new
        assert not mock_session.add.called
        assert existing_record.overall_score == 97 # updated
        assert existing_record.certification_level == "Level A+" # updated
