from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy.future import select
from core.logger import logger
from database.database import db_manager
from database.redis_manager import redis_manager
from events.event_bus import event_bus
from agents.search.search_models import SearchLead
from agents.audit.audit_models import Audit
from agents.audit.interfaces import IAuditAgent
from agents.audit.audit_services import AuditService
from agents.audit.audit_rules import AuditRules

class AuditAgent(IAuditAgent):
    def __init__(self, service = None, rules = None):
        self.service = service or AuditService()
        self.rules = rules or AuditRules()
        self.output_queue_name = "niche_queue"

    async def audit_site(self, lead_id: int, url: str) -> Dict[str, Any]:
        logger.info(f"Starting Website Audit pipeline for lead {lead_id} ('{url}')...")
        
        # Step 1: Verify lead existence and check for duplicate audits
        async with db_manager.session_factory() as session:
            stmt = select(SearchLead).where(SearchLead.id == lead_id)
            result = await session.execute(stmt)
            lead = result.scalars().first()
            
            if not lead:
                logger.error(f"Lead ID {lead_id} not found in database search_leads table.")
                raise ValueError(f"Lead ID {lead_id} does not exist.")
                
            audit_stmt = select(Audit).where(Audit.lead_id == lead_id)
            audit_result = await session.execute(audit_stmt)
            existing_audit = audit_result.scalars().first()
            
            if existing_audit:
                logger.warning(f"Lead {lead_id} has already been audited. Skipping redundant request...")
                return {
                    "lead_id": lead_id,
                    "domain": url,
                    "status": "SKIPPED_DUPLICATE"
                }

        # Step 2: Crawl target site using AuditService
        crawl_payload = await self.service.fetch_page_content(url)
        
        # Step 3: Evaluate scoring matrix using AuditRules
        scores = self.rules.calculate_scores(crawl_payload)
        
        # Step 4: Write audit metrics & update lead status in atomic transaction
        async with db_manager.session_factory() as session:
            async with session.begin():
                stmt = select(SearchLead).where(SearchLead.id == lead_id)
                result = await session.execute(stmt)
                db_lead = result.scalars().first()
                
                new_audit = Audit(
                    lead_id=lead_id,
                    schema_version=scores["schema_version"],
                    audit_rule_version=scores["audit_rule_version"],
                    audit_score=scores["audit_score"],
                    seo_score=scores["seo_score"],
                    mobile_score=scores["mobile_score"],
                    speed_score=scores["speed_score"],
                    trust_score=scores["trust_score"],
                    design_score=scores["design_score"],
                    summary=scores["summary"]
                )
                session.add(new_audit)
                
                if db_lead:
                    db_lead.status = "AUDITED"
                    
            await session.commit()
            
        # Step 5: Push lead payload to Redis downstream queue
        await redis_manager.push_to_queue(self.output_queue_name, url)
        
        # Step 6: Dispatch audit completed payload to Event Bus
        audit_payload = {
            "lead_id": lead_id,
            "domain": url,
            "schema_version": scores["schema_version"],
            "audit_rule_version": scores["audit_rule_version"],
            "audit_score": scores["audit_score"],
            "metrics": {
                "seo": {
                    "score": scores["seo_score"],
                    "title_present": "<title" in crawl_payload["html"].lower(),
                    "meta_description_present": "description" in crawl_payload["html"].lower(),
                    "h1_count": crawl_payload["html"].lower().count("h1") // 2
                },
                "mobile": {
                    "score": scores["mobile_score"],
                    "has_viewport": "viewport" in crawl_payload["html"].lower(),
                    "responsive_layout_detected": "flex" in crawl_payload["html"].lower() or "grid" in crawl_payload["html"].lower()
                },
                "speed": {
                    "score": scores["speed_score"],
                    "response_time_ms": crawl_payload["response_time_ms"],
                    "load_time_ms": crawl_payload["load_time_ms"]
                },
                "trust": {
                    "score": scores["trust_score"],
                    "ssl_valid": crawl_payload["ssl_valid"],
                    "ssl_issuer": crawl_payload["ssl_issuer"],
                    "privacy_policy_present": "privacy" in crawl_payload["html"].lower(),
                    "contact_info_present": "tel:" in crawl_payload["html"].lower() or "phone" in crawl_payload["html"].lower()
                },
                "design": {
                    "score": scores["design_score"],
                    "cta_buttons_detected": "book" in crawl_payload["html"].lower() or "contact" in crawl_payload["html"].lower()
                }
            },
            "summary": scores["summary"],
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
        
        await event_bus.publish("audit_completed", audit_payload)
        logger.info(f"Website Audit complete for lead {lead_id}. Score: {scores['audit_score']}")
        
        return audit_payload
