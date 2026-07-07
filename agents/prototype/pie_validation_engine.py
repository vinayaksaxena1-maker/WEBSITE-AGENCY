import time
from datetime import datetime, timezone
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from agents.prototype.validation_models import PrototypeRelease

# Import sub-modules
from agents.prototype.integration_validator import IntegrationValidator
from agents.prototype.pipeline_validator import PipelineValidator
from agents.prototype.production_checker import ProductionChecker
from agents.prototype.release_manager import ReleaseManager
from agents.prototype.phase_lock import PhaseLock
from agents.prototype.certification_generator import CertificationGenerator
from agents.prototype.final_report import FinalReport

class PIEValidationEngine:
    async def execute_final_validation(self, overall_score: int = 96, version: str = "1.0.0") -> dict:
        """
        Coordinates integration checks, executes final release decisions,
        and logs verification records inside SQLite prototype_release database.
        """
        logger.info("PIEValidationEngine: Commencing final system verification checks.")
        
        # 1. Run integration validator
        is_integrated = IntegrationValidator.check_modules_communication()
        
        # 2. Run pipeline validator
        is_pipeline_ok = PipelineValidator.verify_pipeline_stages()
        
        # 3. Run production readiness checklists
        is_checklist_ok = ProductionChecker.run_checklist_checks()
        
        # Basic validation flags aggregation
        if not is_integrated or not is_pipeline_ok or not is_checklist_ok:
            logger.error("PIEValidationEngine: System verification checks failed!")
            return {
                "success": False,
                "error": "Integration checks or checklist failed."
            }

        # 4. Determine release decision (PASS/FAIL)
        status, is_ready = ReleaseManager.get_release_decision(overall_score)

        # 5. Generate certification metadata
        cert = CertificationGenerator.generate_pie_certificate(overall_score)

        # 6. Generate final report
        report_md = FinalReport.generate_final_report(cert, overall_score)

        # 7. Execute Phase Lock
        PhaseLock.execute_phase_lock()

        # 8. SQLite database updates (Deduplication Check)
        if is_ready:
            try:
                async with db_manager.session_factory() as session:
                    async with session.begin():
                        stmt = select(PrototypeRelease).where(PrototypeRelease.release_version == version)
                        res = await session.execute(stmt)
                        existing = res.scalars().first()

                        if existing:
                            logger.info(f"PIEValidationEngine: Updating existing release record for version {version}...")
                            existing.certification_level = cert["quality_grade"]
                            existing.overall_score = overall_score
                            existing.production_ready = is_ready
                            existing.release_status = status
                            existing.validated_at = datetime.now(timezone.utc)
                        else:
                            logger.info(f"PIEValidationEngine: Creating new release record for version {version}...")
                            new_rel = PrototypeRelease(
                                release_version=version,
                                architecture_version="EDK-V7",
                                certification_level=cert["quality_grade"],
                                overall_score=overall_score,
                                production_ready=is_ready,
                                release_status=status
                            )
                            session.add(new_rel)

                    await session.commit()
            except Exception as e:
                logger.warning(f"PIEValidationEngine: Database release log write failed: {e}")

        return {
            "success": True,
            "certificate": cert,
            "report": report_md,
            "release_status": status,
            "production_ready": is_ready
        }
