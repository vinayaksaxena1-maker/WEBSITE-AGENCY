import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from database.redis_manager import redis_manager
from events.event_bus import event_bus
from agents.search.search_models import SearchLead
from agents.prototype.prototype_models import PrototypeJob, PrototypeResult, PrototypeReport, PrototypeAsset
from agents.prototype.prototype_pipeline import PrototypePipeline

class PrototypeAgent:
    def __init__(self):
        self.output_queue_name = "email_queue"
        self.pipeline = PrototypePipeline()

    async def execute_for_lead(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Executes the Prototype Intelligence Engine pipeline for a specific lead.
        """
        logger.info(f"PrototypeAgent: Starting prototype generation for lead {lead_id} ('{url}')...")

        # Step 1: Verify lead existence
        async with db_manager.session_factory() as session:
            stmt = select(SearchLead).where(SearchLead.id == lead_id)
            result = await session.execute(stmt)
            lead = result.scalars().first()

            if not lead:
                logger.error(f"PrototypeAgent: Lead ID {lead_id} not found in search_leads table.")
                raise ValueError(f"Lead ID {lead_id} does not exist.")

            niche = lead.niche

        # Step 2: Register/Update PrototypeJob in Database (Deduplication Check)
        job_id = None
        async with db_manager.session_factory() as session:
            async with session.begin():
                job_stmt = select(PrototypeJob).where(PrototypeJob.lead_id == lead_id)
                job_result = await session.execute(job_stmt)
                existing_job = job_result.scalars().first()

                if existing_job:
                    logger.warning(f"PrototypeAgent: Job already exists for lead {lead_id}. Updating existing record...")
                    existing_job.status = "RUNNING"
                    existing_job.theme = None
                    existing_job.started_at = datetime.now(timezone.utc)
                    existing_job.completed_at = None
                    job_id = existing_job.id
                else:
                    new_job = PrototypeJob(
                        lead_id=lead_id,
                        website_url=url,
                        status="RUNNING",
                        started_at=datetime.now(timezone.utc)
                    )
                    session.add(new_job)
                    await session.flush()  # To get new_job.id before commit
                    job_id = new_job.id

            await session.commit()

        # Step 3: Run the pipeline
        pipeline_res = await self.pipeline.execute_pipeline(url, niche, job_id=job_id)
        success = pipeline_res.get("success", False)

        # Step 4: Save results and update status atomically
        async with db_manager.session_factory() as session:
            async with session.begin():
                # Re-fetch the job in the current session
                job_stmt = select(PrototypeJob).where(PrototypeJob.id == job_id)
                job_res = await session.execute(job_stmt)
                db_job = job_res.scalars().first()

                lead_stmt = select(SearchLead).where(SearchLead.id == lead_id)
                lead_res = await session.execute(lead_stmt)
                db_lead = lead_res.scalars().first()

                # Update job status
                if db_job:
                    db_job.status = "COMPLETED" if success else "FAILED"
                    db_job.completed_at = datetime.now(timezone.utc)
                    if success:
                        db_job.theme = pipeline_res.get("theme_name")

                # Update lead status
                if db_lead:
                    db_lead.status = "PROTOTYPED" if success else "PROTOTYPING_FAILED"

                if success:
                    # Upsert Result
                    res_stmt = select(PrototypeResult).where(PrototypeResult.job_id == job_id)
                    res_result = await session.execute(res_stmt)
                    existing_res = res_result.scalars().first()

                    if existing_res:
                        existing_res.html_path = pipeline_res.get("html_path")
                        existing_res.css_path = pipeline_res.get("css_path")
                        existing_res.preview_path = pipeline_res.get("preview_path")
                        existing_res.quality_score = pipeline_res.get("quality_score")
                        existing_res.generation_time = pipeline_res.get("execution_time")
                    else:
                        new_res = PrototypeResult(
                            job_id=job_id,
                            html_path=pipeline_res.get("html_path"),
                            css_path=pipeline_res.get("css_path"),
                            preview_path=pipeline_res.get("preview_path"),
                            quality_score=pipeline_res.get("quality_score"),
                            generation_time=pipeline_res.get("execution_time")
                        )
                        session.add(new_res)

                    # Upsert Report
                    rep_stmt = select(PrototypeReport).where(PrototypeReport.job_id == job_id)
                    rep_res = await session.execute(rep_stmt)
                    existing_rep = rep_res.scalars().first()

                    summary_str = f"Prototype generated for {url}. Niche: {niche}."
                    imp_str = json.dumps(pipeline_res.get("improvements", []))
                    war_str = json.dumps(pipeline_res.get("warnings", []))
                    rec_str = json.dumps(pipeline_res.get("recommendations", []))

                    if existing_rep:
                        existing_rep.summary = summary_str
                        existing_rep.improvements = imp_str
                        existing_rep.warnings = war_str
                        existing_rep.recommendations = rec_str
                    else:
                        new_rep = PrototypeReport(
                            job_id=job_id,
                            summary=summary_str,
                            improvements=imp_str,
                            warnings=war_str,
                            recommendations=rec_str
                        )
                        session.add(new_rep)

                    # Delete existing assets for this job (preventing duplicates on rerun)
                    del_stmt = select(PrototypeAsset).where(PrototypeAsset.job_id == job_id)
                    del_res = await session.execute(del_stmt)
                    for asset in del_res.scalars().all():
                        session.delete(asset)

                    # Add new assets
                    for asset_data in pipeline_res.get("assets", []):
                        new_asset = PrototypeAsset(
                            job_id=job_id,
                            asset_type=asset_data.get("type"),
                            asset_path=asset_data.get("path")
                        )
                        session.add(new_asset)

            await session.commit()

        # Step 5: Downstream Actions and Event Bus
        event_payload = {
            "lead_id": lead_id,
            "domain": url,
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }

        if success:
            event_payload.update({
                "job_id": job_id,
                "html_path": pipeline_res.get("html_path"),
                "preview_path": pipeline_res.get("preview_path"),
                "quality_score": pipeline_res.get("quality_score"),
                "theme_name": pipeline_res.get("theme_name")
            })

            logger.info(f"PrototypeAgent: Successfully generated prototype for lead {lead_id}. Status updated to PROTOTYPED.")

            # Push lead to Redis downstream queue
            try:
                await redis_manager.push_to_queue(self.output_queue_name, url)
                logger.info(f"PrototypeAgent: Lead '{url}' enqueued into downstream '{self.output_queue_name}'.")
            except Exception as e:
                logger.warning(f"PrototypeAgent: Failed to push to Redis downstream queue '{self.output_queue_name}': {e}")
        else:
            event_payload["error"] = pipeline_res.get("error", "Unknown pipeline error")
            logger.warning(f"PrototypeAgent: Prototype generation failed for lead {lead_id}. Status updated to PROTOTYPING_FAILED.")

        # Publish to Event Bus
        await event_bus.publish("prototype_generated", event_payload)

        return event_payload
