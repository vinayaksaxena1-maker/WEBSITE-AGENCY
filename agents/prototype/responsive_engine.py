import time
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from agents.prototype.prototype_models import PrototypeResponsive

# Import Responsive Sub-engine components
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

class ResponsiveEngine:
    async def make_responsive(self, components: List[Dict[str, Any]], job_id: int = None) -> List[Dict[str, Any]]:
        """
        Enforces mobile viewport styling overrides for Tailwind/CSS elements,
        and saves responsive blueprints to SQLite databases if job_id is provided.
        """
        start_time = time.time()
        logger.info("ResponsiveEngine: Compiling responsive breakpoint blueprints...")

        # 1. Fetch screen layout viewports definition profile
        viewports = BreakpointManager.get_breakpoints()

        # 2. Iterate and generate responsive specifications per device screen size
        blueprint = {}
        for device, config in viewports.items():
            col_collapse = GridAdapter.adapt_grid(config["grid_columns"], device)
            pad_val = ContainerAdapter.get_padding_rules(device)
            card_layout = ComponentAdapter.adapt_card_layout(device)
            nav_style = NavigationAdapter.get_navigation_style(device)
            font_size = TypographyScaler.get_scaled_font(32, device)
            gap_size = SpacingScaler.get_scaled_gap(16, device)

            blueprint[device] = {
                "min_width": config["min_width"],
                "container_width": config["container_width"],
                "adapted_columns": col_collapse,
                "padding_rule": pad_val,
                "card_layout": card_layout,
                "navigation_style": nav_style,
                "heading_font_size": font_size,
                "grid_gap": gap_size
            }

        # 3. Validate breakpoint rules completeness
        score, status = ResponsiveValidator.validate_coverage(blueprint)

        elapsed = time.time() - start_time
        logger.info(f"ResponsiveEngine: Completed adaptation specs in {elapsed:.3f} seconds. Score: {score}/100")

        # 4. Format markdown report
        report_md = ResponsiveReport.generate_report(blueprint, score, status, elapsed)

        # 5. SQLite database updates (Deduplication Check)
        if job_id is not None:
            try:
                # Serialized JSON representations
                breakpoint_json = json.dumps(blueprint)
                device_json = json.dumps(list(viewports.keys()))

                async with db_manager.session_factory() as session:
                    async with session.begin():
                        stmt = select(PrototypeResponsive).where(PrototypeResponsive.job_id == job_id)
                        res = await session.execute(stmt)
                        existing = res.scalars().first()

                        if existing:
                            logger.info(f"ResponsiveEngine: Updating existing responsive blueprint for job {job_id}...")
                            existing.breakpoint_profile = breakpoint_json
                            existing.device_support = device_json
                            existing.responsive_score = score
                            existing.validation_status = status
                            existing.execution_time = elapsed
                            existing.created_at = datetime.now(timezone.utc)
                        else:
                            logger.info(f"ResponsiveEngine: Creating new responsive blueprint for job {job_id}...")
                            new_resp = PrototypeResponsive(
                                job_id=job_id,
                                breakpoint_profile=breakpoint_json,
                                device_support=device_json,
                                responsive_score=score,
                                validation_status=status,
                                execution_time=elapsed
                            )
                            session.add(new_resp)

                    await session.commit()
            except Exception as e:
                logger.warning(f"ResponsiveEngine: Database responsive write failed: {e}")

        # Inject styling classes for components compatibility with legacy stubs
        for comp in components:
            comp["classes"] = comp.get("classes", "") + " w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
            comp["responsive_blueprint"] = blueprint
            comp["responsive_score"] = score
            comp["responsive_report"] = report_md

        return components
