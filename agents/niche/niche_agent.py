from typing import Dict, Any
from sqlalchemy import select
from database.database import db_manager
from database.redis_manager import redis_manager
from events.event_bus import event_bus
from core.logger import logger
from agents.search.search_models import SearchLead
from agents.niche.niche_models import BusinessProfile
from agents.niche.classifier import HybridClassifier
from agents.niche.theme_mapper import ThemeMapper
from agents.niche.interfaces import INicheAgent
from agents.audit.audit_services import AuditService
from datetime import datetime, timezone

class NicheAgent(INicheAgent):
    def __init__(self):
        self.classifier = HybridClassifier()
        self.theme_mapper = ThemeMapper()
        self.crawler_service = AuditService()
        self.output_queue_name = "scoring_queue"

    async def detect_niche(self, lead_id: int, url: str, html_content: str = None) -> Dict[str, Any]:
        logger.info(f"Starting Niche Detection pipeline for lead {lead_id} ('{url}')...")

        # Step 1: Verify lead existence
        async with db_manager.session_factory() as session:
            stmt = select(SearchLead).where(SearchLead.id == lead_id)
            result = await session.execute(stmt)
            lead = result.scalars().first()

            if not lead:
                logger.error(f"Lead ID {lead_id} not found in database search_leads table.")
                raise ValueError(f"Lead ID {lead_id} does not exist.")

        # Step 2: Fetch HTML page content if not provided in parameter
        if not html_content:
            logger.info(f"Page content not provided. Crawling '{url}' dynamically...")
            crawl_data = await self.crawler_service.fetch_page_content(url)
            html_content = crawl_data.get("html", "")

        # Step 3: Run Hybrid Classifier
        industry, confidence = self.classifier.classify(html_content)

        # Step 4: Map recommended theme layout
        recommended_theme = self.theme_mapper.recommend_theme(industry)

        # Step 5: Save business profile & update lead status in single atomic transaction
        async with db_manager.session_factory() as session:
            async with session.begin():
                # Check for existing profile to avoid unique constraint crashes
                profile_stmt = select(BusinessProfile).where(BusinessProfile.lead_id == lead_id)
                profile_result = await session.execute(profile_stmt)
                existing_profile = profile_result.scalars().first()

                # Re-fetch lead object inside transaction scope to update its status
                lead_stmt = select(SearchLead).where(SearchLead.id == lead_id)
                lead_result = await session.execute(lead_stmt)
                db_lead = lead_result.scalars().first()

                if existing_profile:
                    logger.warning(f"Business Profile for lead {lead_id} already exists. Updating existing record...")
                    existing_profile.industry = industry
                    existing_profile.confidence = confidence
                    existing_profile.recommended_theme = recommended_theme
                    existing_profile.updated_at = datetime.now(timezone.utc)
                else:
                    new_profile = BusinessProfile(
                        lead_id=lead_id,
                        industry=industry,
                        confidence=confidence,
                        recommended_theme=recommended_theme
                    )
                    session.add(new_profile)

                if db_lead:
                    db_lead.status = "CLASSIFIED"

            await session.commit()

        logger.info(f"Business Profile saved successfully. Industry: '{industry}' (Confidence: {confidence:.2f})")

        # Step 6: Push target lead payload to downstream Redis scoring queue
        await redis_manager.push_to_queue(self.output_queue_name, url)

        # Step 7: Dispatch completion payload to Event Bus
        event_payload = {
            "lead_id": lead_id,
            "domain": url,
            "industry": industry,
            "confidence": confidence,
            "recommended_theme": recommended_theme,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
        await event_bus.publish("niche_detected", event_payload)

        return event_payload
