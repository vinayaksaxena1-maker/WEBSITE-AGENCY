import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy import select, delete
from core.logger import logger
from database.database import db_manager
from agents.prototype.prototype_models import PrototypeComponent

# Import Component Sub-engine components
from agents.prototype.component_library import COMPONENTS_LIBRARY
from agents.prototype.component_selector import ComponentSelector
from agents.prototype.component_tree import ComponentTree
from agents.prototype.variant_selector import VariantSelector
from agents.prototype.dependency_validator import DependencyValidator
from agents.prototype.component_validator import ComponentValidator
from agents.prototype.component_report import ComponentReport

class ComponentEngine:
    async def assemble_components(self, layout: Dict[str, Any], theme: Dict[str, Any] = None, job_id: int = None) -> List[Dict[str, Any]]:
        """
        Builds, selects, validates, and chains reusable component trees.
        Saves output states into SQLite databases if job_id is provided.
        """
        start_time = time.time()
        logger.info("ComponentEngine: Initiating component layouts compilation...")

        if theme is None:
            theme = {"category": "Modern Business"}

        # 1. Selector Mapping
        raw_sections = []
        for item in layout.get("structure", []):
            raw_sections.append({
                "type": item.get("section", "section"),
                "original_item": item
            })

        components = ComponentSelector.select_components(raw_sections)

        # 2. Variant selection and mapping
        for comp, sec_item in zip(components, raw_sections):
            orig = sec_item["original_item"]
            # If the item had a variant specified in structure (e.g. from legacy tests), use that; else deduce it
            legacy_var = orig.get("layout")
            if legacy_var:
                comp["variant"] = legacy_var
            else:
                comp["variant"] = VariantSelector.select_variant(comp["name"], theme)

        # 3. Dependency validation
        dep_errors = DependencyValidator.validate_dependencies(components)

        # 4. Standard validation loop
        validation_summary = ComponentValidator.validate_components(components)

        # 5. Tree build (with deep safeguarding <10 layers limit)
        tree = ComponentTree.build_tree(components)

        # 6. Report formatting
        report_md = ComponentReport.generate_report(components, tree, validation_summary)

        # 7. Convert to backward-compatible return representation
        returned_components = []
        for comp in components:
            short_type = comp["name"].replace("Component", "").lower()
            classes = "p-8 md:p-16 border-b border-gray-100"
            html_snippet = f"<section class='{short_type}-section'><h2>{comp['name'].capitalize()} Block</h2></section>"

            returned_components.append({
                "type": short_type,
                "variant": comp["variant"],
                "classes": classes,
                "html_snippet": html_snippet,
                # EDK properties
                "instance_id": comp["instance_id"],
                "name": comp["name"],
                "priority": comp["priority"],
                "dependencies": ",".join(comp["dependencies"]),
                "responsive_ready": True,
                "accessibility_ready": True
            })

        elapsed = time.time() - start_time
        logger.info(f"ComponentEngine: Component assembly completed in {elapsed:.3f} seconds.")

        # 8. SQLite Database writes with deduplication refresh check
        if job_id is not None:
            try:
                async with db_manager.session_factory() as session:
                    async with session.begin():
                        # Delete existing components for this job to refresh (deduplication)
                        stmt_del = delete(PrototypeComponent).where(PrototypeComponent.job_id == job_id)
                        await session.execute(stmt_del)

                        # Insert refreshed components
                        for rc in returned_components:
                            new_comp = PrototypeComponent(
                                job_id=job_id,
                                component_name=rc["name"],
                                variant=rc["variant"],
                                theme=theme.get("name", "default-theme"),
                                priority=rc["priority"],
                                dependencies=rc["dependencies"],
                                responsive_ready=rc["responsive_ready"],
                                accessibility_ready=rc["accessibility_ready"],
                                status="COMPILED"
                            )
                            session.add(new_comp)

                    await session.commit()
            except Exception as e:
                logger.warning(f"ComponentEngine: Database component write failed: {e}")

        return returned_components
