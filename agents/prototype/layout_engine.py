import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from agents.prototype.prototype_models import PrototypeTemplate

# Import Layout Sub-engine components
from agents.prototype.layout_selector import LayoutSelector
from agents.prototype.grid_builder import GridBuilder
from agents.prototype.sequence_sorter import SequenceSorter
from agents.prototype.spacing_rules import SpacingRules
from agents.prototype.layout_validator import LayoutValidator

class LayoutEngine:
    async def create_layout_grid(self, sections: List[Any], theme: Dict[str, Any], job_id: int = None) -> Dict[str, Any]:
        """
        Plans layouts grid structures, column widths, re-orders sections flow,
        and saves audits configurations to the database.
        """
        start_time = time.time()
        logger.info("LayoutEngine: Compiling layout structural grid blueprint...")

        # 1. Standardise inputs list (handles list of strings and list of dicts)
        normalized_sections = []
        for s in sections:
            if isinstance(s, str):
                normalized_sections.append({"section": s, "layout": "default"})
            elif isinstance(s, dict):
                normalized_sections.append(s.copy())

        # 2. Validation & Repair (Auto-injection of Header/Footer)
        repaired = LayoutValidator.validate_and_repair(normalized_sections)

        # 3. Sequencing sorter
        sorted_sections = SequenceSorter.sort_sequence(repaired)

        # 4. Selector mapping
        niche = theme.get("name", "Modern Corporate").split("-")[0]
        layout_type = LayoutSelector.select_layout_type(niche)

        # 5. Grid Builder & Columns translation
        columns_count = 1
        # Set dynamic columns based on content count to simulate translation matrices
        if any(c["section"] in ("services", "features", "products") for c in sorted_sections):
            columns_count = 3

        tailwind_grid_class = GridBuilder.get_tailwind_classes(columns_count)

        # 6. Spacing compiler
        spacings = SpacingRules.get_spacing_rules(theme)

        elapsed = time.time() - start_time
        logger.info(f"LayoutEngine: Layout grid blueprint generated in {elapsed:.3f} seconds.")

        # Returned Blueprint structure (preserves legacy format layout_type, structure, theme_name)
        blueprint = {
            "layout_type": layout_type,
            "structure": sorted_sections,
            "columns_count": columns_count,
            "tailwind_grid_class": tailwind_grid_class,
            "spacing_rules": spacings,
            "theme_name": theme.get("name"),
            "status": "STRUCTURED"
        }

        # 7. SQLite Database updates (Deduplication Check)
        if job_id is not None:
            try:
                async with db_manager.session_factory() as session:
                    async with session.begin():
                        stmt = select(PrototypeTemplate).where(PrototypeTemplate.job_id == job_id)
                        res = await session.execute(stmt)
                        existing = res.scalars().first()

                        sequence_str = ",".join(s["section"] for s in sorted_sections)
                        spacing_str = json.dumps(spacings)

                        if existing:
                            logger.info(f"LayoutEngine: Updating existing layout template record for job {job_id}...")
                            existing.layout_type = layout_type
                            existing.columns_count = columns_count
                            existing.section_sequence = sequence_str
                            existing.tailwind_grid_class = tailwind_grid_class
                            existing.spacing_rules = spacing_str
                            existing.status = "STRUCTURED"
                            existing.created_at = datetime.now(timezone.utc)
                        else:
                            logger.info(f"LayoutEngine: Creating new layout template record for job {job_id}...")
                            new_template = PrototypeTemplate(
                                job_id=job_id,
                                layout_type=layout_type,
                                columns_count=columns_count,
                                section_sequence=sequence_str,
                                tailwind_grid_class=tailwind_grid_class,
                                spacing_rules=spacing_str,
                                status="STRUCTURED"
                            )
                            session.add(new_template)

                    await session.commit()
            except Exception as e:
                logger.warning(f"LayoutEngine: Database layout write failed: {e}")

        return blueprint
