import os
import time
from datetime import datetime, timezone
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from agents.prototype.prototype_models import PrototypeExport

# Import sub-modules
from agents.prototype.export_validator import ExportValidator
from agents.prototype.package_builder import PackageBuilder
from agents.prototype.manifest_generator import ManifestGenerator
from agents.prototype.version_manager import VersionManager
from agents.prototype.checksum_generator import ChecksumGenerator
from agents.prototype.asset_packager import AssetPackager
from agents.prototype.integrity_checker import IntegrityChecker
from agents.prototype.export_report import ExportReport

class ExportEngine:
    def __init__(self, export_dir: str = "output/exports"):
        self.export_dir = export_dir

    async def export_prototype(self, html_path: str, css_path: str, theme_name: str, job_id: int = None) -> dict:
        """
        Validates, packages static builds folders into ZIP, compiles integrity SHA-256 signatures,
        and logs transaction details inside the SQLite prototype_exports table.
        """
        logger.info(f"ExportEngine: Commencing export process for job {job_id}")
        
        # 1. Read files and validate (Credential Leak scan)
        html_content = ""
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        css_content = ""
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()

        is_html_clean = ExportValidator.scan_for_credentials(html_content)
        is_css_clean = ExportValidator.scan_for_credentials(css_content)

        if not is_html_clean or not is_css_clean:
            logger.error("ExportEngine: SECURITY WARNING: Credentials leak detected in static code blocks! Aborting export.")
            return {
                "success": False,
                "error": "Credentials leak detected in code assets."
            }

        # 2. Setup destination workspace directories
        temp_dir = os.path.join(self.export_dir, "temp_build")
        os.makedirs(temp_dir, exist_ok=True)

        # 3. Collect assets
        AssetPackager.collect_assets(html_path, css_path, temp_dir)

        # 4. Generate manifest.json
        manifest_meta = {
            "version": "1.0.0",
            "generator_version": "PIE-1.0",
            "theme": theme_name,
            "exported_at": datetime.now(timezone.utc).isoformat()
        }
        manifest_path = os.path.join(temp_dir, "manifest.json")
        ManifestGenerator.generate_manifest(manifest_meta, manifest_path)

        # 5. Build ZIP Package
        zip_output_path = os.path.join(self.export_dir, f"prototype_job_{job_id or 'unknown'}.zip")
        pkg_size = PackageBuilder.create_zip(temp_dir, zip_output_path)

        # 6. Verify ZIP integrity
        is_valid = IntegrityChecker.verify_zip_integrity(zip_output_path)
        if not is_valid:
            logger.error("ExportEngine: Generated ZIP file integrity check failed!")
            return {
                "success": False,
                "error": "Integrity check failed."
            }

        # 7. Generate checksum signature
        hash_val = ChecksumGenerator.calculate_sha256(zip_output_path)

        # Clean up temp folder
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except Exception:
            pass

        # 8. SQLite database updates (Deduplication Check)
        status = "COMPLETED"
        val_status = "PASSED"
        
        if job_id is not None:
            try:
                async with db_manager.session_factory() as session:
                    async with session.begin():
                        stmt = select(PrototypeExport).where(PrototypeExport.job_id == job_id)
                        res = await session.execute(stmt)
                        existing = res.scalars().first()

                        if existing:
                            logger.info(f"ExportEngine: Updating existing export record for job {job_id}...")
                            existing.export_version = "1.0.0"
                            existing.package_name = os.path.basename(zip_output_path)
                            existing.package_size = pkg_size
                            existing.checksum = hash_val
                            existing.export_status = status
                            existing.validation_status = val_status
                            existing.generated_at = datetime.now(timezone.utc)
                        else:
                            logger.info(f"ExportEngine: Creating new export record for job {job_id}...")
                            new_exp = PrototypeExport(
                                job_id=job_id,
                                export_version="1.0.0",
                                package_name=os.path.basename(zip_output_path),
                                package_size=pkg_size,
                                checksum=hash_val,
                                export_status=status,
                                validation_status=val_status
                            )
                            session.add(new_exp)

                    await session.commit()
            except Exception as e:
                logger.warning(f"ExportEngine: Database export log write failed: {e}")

        return {
            "success": True,
            "zip_path": zip_output_path,
            "package_size": pkg_size,
            "checksum": hash_val,
            "manifest": manifest_meta
        }
