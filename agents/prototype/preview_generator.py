import os
import time
from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from agents.prototype.prototype_models import PrototypePreview

# Import sub-modules
from agents.prototype.preview_server import PreviewServer
from agents.prototype.render_validator import RenderValidator
from agents.prototype.device_renderer import DeviceRenderer
from agents.prototype.comparison_engine import ComparisonEngine
from agents.prototype.preview_capture import PreviewCapture
from agents.prototype.preview_metadata import PreviewMetadata
from agents.prototype.preview_report import PreviewReport

class PreviewGenerator:
    def __init__(self, output_dir: str = "output/prototypes/previews"):
        self.output_dir = output_dir

    async def generate_preview(self, html_path: str, job_id: int = None) -> str:
        """
        Loads the generated HTML in browser and captures high-resolution previews,
        updating the prototype_previews database log table if job_id is provided.
        """
        logger.info(f"PreviewGenerator: Initiating visual captures loop for '{html_path}'")
        
        # 1. Spawn temporary local preview server session
        server = PreviewServer(directory=os.path.dirname(html_path), port=8088)
        server.start()

        time.sleep(0.5)  # Let server bind cleanly

        # 2. Get viewport sizes
        viewports = DeviceRenderer.get_viewports()
        captured_paths = {}

        # 3. Capture screenshots per device size
        for device, (w, h) in viewports.items():
            out_file = f"{self.output_dir}/{device}_preview.png"
            local_url = f"http://localhost:{server.port}/{os.path.basename(html_path)}"
            PreviewCapture.capture_screenshot(local_url, out_file, w, h)
            captured_paths[device] = out_file

        # 4. Compile visual comparison overlay
        comp_file = f"{self.output_dir}/side_by_side_comparison.png"
        ComparisonEngine.compile_comparison(
            before_path="output/crawler_target.png",  # mock target crawler placeholder
            after_path=captured_paths.get("desktop", ""),
            output_path=comp_file
        )

        # 5. Clean up server sockets sessions
        server.stop()

        # 6. Execute layout validations checks
        score, status = RenderValidator.validate_layout(html_path)

        # 7. SQLite database updates (Deduplication Check)
        if job_id is not None:
            try:
                async with db_manager.session_factory() as session:
                    async with session.begin():
                        stmt = select(PrototypePreview).where(PrototypePreview.job_id == job_id)
                        res = await session.execute(stmt)
                        existing = res.scalars().first()

                        if existing:
                            logger.info(f"PreviewGenerator: Updating existing preview records for job {job_id}...")
                            existing.preview_version = "1.0.0"
                            existing.desktop_image = captured_paths.get("desktop")
                            existing.laptop_image = captured_paths.get("laptop")
                            existing.tablet_image = captured_paths.get("tablet")
                            existing.mobile_image = captured_paths.get("mobile")
                            existing.comparison_image = comp_file
                            existing.preview_score = score
                            existing.status = status
                            existing.created_at = datetime.now(timezone.utc)
                        else:
                            logger.info(f"PreviewGenerator: Creating new preview records for job {job_id}...")
                            new_prev = PrototypePreview(
                                job_id=job_id,
                                preview_version="1.0.0",
                                desktop_image=captured_paths.get("desktop"),
                                laptop_image=captured_paths.get("laptop"),
                                tablet_image=captured_paths.get("tablet"),
                                mobile_image=captured_paths.get("mobile"),
                                comparison_image=comp_file,
                                preview_score=score,
                                status=status
                            )
                            session.add(new_prev)

                    await session.commit()
            except Exception as e:
                logger.warning(f"PreviewGenerator: Database preview log write failed: {e}")

        # Create mock_preview.png (by copying desktop_preview.png)
        mock_preview_path = f"{self.output_dir}/mock_preview.png"
        try:
            import shutil
            shutil.copyfile(captured_paths.get("desktop"), mock_preview_path)
        except Exception as e:
            logger.warning(f"PreviewGenerator: Failed to copy mock_preview: {e}")

        # Returns primary preview target path
        return mock_preview_path
