from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy import select
from database.database import db_manager
from database.redis_manager import redis_manager
from events.event_bus import event_bus
from core.logger import logger
from agents.search.search_models import SearchLead
from agents.audit.audit_models import Audit
from agents.niche.niche_models import BusinessProfile
from agents.scoring.scoring_models import LeadScore
from agents.scoring.scoring_calculator import ScoringCalculator
from agents.scoring.business_value_calculator import BusinessValueCalculator
from agents.scoring.interfaces import IScoringAgent

class ScoringAgent(IScoringAgent):
    def __init__(self):
        self.scoring_calculator = ScoringCalculator()
        self.business_value_calculator = BusinessValueCalculator()
        self.output_queue_name = "contact_queue"

    async def score_lead(self, lead_id: int, url: str) -> Dict[str, Any]:
        logger.info(f"Starting Lead Scoring pipeline for lead {lead_id} ('{url}')...")

        # Step 1: Verify lead existence
        async with db_manager.session_factory() as session:
            stmt = select(SearchLead).where(SearchLead.id == lead_id)
            result = await session.execute(stmt)
            lead = result.scalars().first()

            if not lead:
                logger.error(f"Lead ID {lead_id} not found in database search_leads table.")
                raise ValueError(f"Lead ID {lead_id} does not exist.")

        # Step 2: Fetch Audit and BusinessProfile
        async with db_manager.session_factory() as session:
            audit_stmt = select(Audit).where(Audit.lead_id == lead_id)
            audit_result = await session.execute(audit_stmt)
            audit = audit_result.scalars().first()

            profile_stmt = select(BusinessProfile).where(BusinessProfile.lead_id == lead_id)
            profile_result = await session.execute(profile_stmt)
            business_profile = profile_result.scalars().first()

        # Step 3: Run Calculators
        if not audit:
            logger.warning(f"No audit data found for lead {lead_id}. Proceeding with defaults.")
        if not business_profile:
            logger.warning(f"No business profile found for lead {lead_id}. Proceeding with defaults.")

        lead_score, opportunities = self.scoring_calculator.calculate_lead_score(audit)
        bvi = self.business_value_calculator.calculate_business_value_index(audit, business_profile, lead_score)

        # Step 4: Map priority levels and decisions
        if lead_score <= 30:
            priority_level = "Low Priority"
            ai_processing_decision = "IGNORE"
        elif lead_score <= 60:
            priority_level = "Medium Priority"
            ai_processing_decision = "MANUAL_REVIEW"
        elif lead_score <= 80:
            priority_level = "High Priority"
            ai_processing_decision = "PROCEED"
        else:
            priority_level = "Premium Lead"
            ai_processing_decision = "IMMEDIATE_PROCESSING"

        opportunities_str = ",".join(opportunities) if opportunities else ""

        # Step 5: Save/update score & update lead status in single atomic transaction
        async with db_manager.session_factory() as session:
            async with session.begin():
                score_stmt = select(LeadScore).where(LeadScore.lead_id == lead_id)
                score_result = await session.execute(score_stmt)
                existing_score = score_result.scalars().first()

                lead_stmt = select(SearchLead).where(SearchLead.id == lead_id)
                lead_result = await session.execute(lead_stmt)
                db_lead = lead_result.scalars().first()

                if existing_score:
                    logger.warning(f"Lead Score for lead {lead_id} already exists. Updating existing record...")
                    existing_score.lead_score = lead_score
                    existing_score.priority_level = priority_level
                    existing_score.business_value_index = bvi
                    existing_score.ai_processing_decision = ai_processing_decision
                    existing_score.improvement_opportunities = opportunities_str
                    existing_score.updated_at = datetime.now(timezone.utc)
                else:
                    new_score = LeadScore(
                        lead_id=lead_id,
                        lead_score=lead_score,
                        priority_level=priority_level,
                        business_value_index=bvi,
                        ai_processing_decision=ai_processing_decision,
                        improvement_opportunities=opportunities_str
                    )
                    session.add(new_score)

                if db_lead:
                    db_lead.status = "SCORED"

            await session.commit()

        logger.info(f"Lead Score saved successfully for lead {lead_id}. Score: {lead_score}, Priority: {priority_level}, BVI: {bvi}")

        # Step 6: Push target lead payload to downstream Redis queue
        await redis_manager.push_to_queue(self.output_queue_name, url)

        # Step 7: Dispatch completion payload to Event Bus
        event_payload = {
            "lead_id": lead_id,
            "domain": url,
            "lead_score": lead_score,
            "priority_level": priority_level,
            "business_value_index": bvi,
            "ai_processing_decision": ai_processing_decision,
            "improvement_opportunities": opportunities,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
        await event_bus.publish("lead_scored", event_payload)

        return event_payload
