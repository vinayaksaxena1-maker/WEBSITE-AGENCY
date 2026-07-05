import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from database.redis_manager import redis_manager
from events.event_bus import event_bus
from agents.search.search_models import SearchLead
from agents.contact.contact_models import Contact
from agents.email_validation.validation_models import ValidatedEmail
from agents.email_validation.syntax_validator import SyntaxValidator
from agents.email_validation.dns_validator import DNSValidator
from agents.email_validation.mx_validator import MXValidator
from agents.email_validation.disposable_detector import DisposableDetector
from agents.email_validation.role_detector import RoleDetector
from agents.email_validation.quality_score import QualityScoreCalculator
from agents.email_validation.confidence_engine import ConfidenceEngine

class EmailValidationAgent:
    def __init__(self):
        self.output_queue_name = "prototype_queue"

    async def validate_single_email(self, email: str, website_domain: str) -> Dict[str, Any]:
        """
        Validates a single email address, returning its validation metrics.
        """
        if not email:
            return {
                "email": "",
                "syntax_valid": False,
                "dns_valid": False,
                "mx_valid": False,
                "disposable": False,
                "role_based": False,
                "quality_score": 0,
                "classification": "Invalid",
                "confidence": 0.0,
                "recommended_action": "Reject"
            }
            
        # Stage 1: Syntax check
        is_syntax_valid = SyntaxValidator.validate(email)
        
        # Split local and domain
        domain = ""
        if is_syntax_valid:
            parts = email.split("@")
            if len(parts) == 2:
                domain = parts[1]
                
        # Stage 2 & 3 & 4 & 5 & 6 executed in parallel with 1.8 seconds max timeout
        is_dns_valid = False
        is_mx_valid = False
        is_disposable = False
        is_role_based = False
        
        if is_syntax_valid and domain:
            try:
                # Concurrently run DNS validation, MX validation, disposable check, and role check
                dns_task = DNSValidator.validate_domain(domain, timeout=1.5)
                mx_task = MXValidator.validate_mx(domain, timeout=1.5)
                
                dns_res, mx_res = await asyncio.gather(dns_task, mx_task)
                is_dns_valid = dns_res
                is_mx_valid = mx_res
            except Exception as e:
                logger.warning(f"DNS/MX validation error for '{email}': {e}")
                
            is_disposable = DisposableDetector.is_disposable(domain)
            is_role_based = RoleDetector.is_role_based(email)
            
        # Calculate Quality Score & Confidence
        quality = QualityScoreCalculator.calculate(
            email=email,
            is_syntax_valid=is_syntax_valid,
            is_dns_valid=is_dns_valid,
            is_mx_valid=is_mx_valid,
            is_disposable=is_disposable,
            is_role_based=is_role_based,
            website_domain=website_domain
        )
        
        classification, confidence, action = ConfidenceEngine.get_classification_and_action(quality, is_disposable)
        
        return {
            "email": email,
            "syntax_valid": is_syntax_valid,
            "dns_valid": is_dns_valid,
            "mx_valid": is_mx_valid,
            "disposable": is_disposable,
            "role_based": is_role_based,
            "quality_score": quality,
            "classification": classification,
            "confidence": confidence,
            "recommended_action": action
        }

    async def validate_lead_emails(self, lead_id: int, url: str) -> Dict[str, Any]:
        logger.info(f"Starting Email Validation pipeline for lead {lead_id} ('{url}')...")
        
        # Step 1: Verify lead existence and fetch contacts
        async with db_manager.session_factory() as session:
            stmt = select(SearchLead).where(SearchLead.id == lead_id)
            result = await session.execute(stmt)
            lead = result.scalars().first()
            
            if not lead:
                logger.error(f"Lead ID {lead_id} not found in database search_leads table.")
                raise ValueError(f"Lead ID {lead_id} does not exist.")
                
            c_stmt = select(Contact).where(Contact.lead_id == lead_id)
            c_res = await session.execute(c_stmt)
            contacts = c_res.scalars().first()
            
        if not contacts:
            logger.warning(f"No contacts record found for lead {lead_id}. Aborting email validation.")
            return {"lead_id": lead_id, "domain": url, "success": False, "reason": "No Contact Record"}
            
        emails_to_validate = []
        if contacts.primary_email:
            emails_to_validate.append(contacts.primary_email)
        if contacts.secondary_email:
            emails_to_validate.append(contacts.secondary_email)
            
        if not emails_to_validate:
            logger.warning(f"No emails extracted for lead {lead_id}. Aborting email validation.")
            return {"lead_id": lead_id, "domain": url, "success": False, "reason": "No Emails Extracted"}
            
        # Step 2: Validate emails concurrently with strict timeout (1.9 seconds total)
        results = []
        try:
            tasks = [self.validate_single_email(email, url) for email in emails_to_validate]
            results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=1.9)
        except asyncio.TimeoutError:
            logger.error(f"Timeout: Email validation execution timed out for lead {lead_id}.")
        except Exception as e:
            logger.error(f"Failure: Email validation execution failed for lead {lead_id}: {e}", exc_info=True)
            
        # Select best email (highest quality score)
        best_email = None
        if results:
            # Sort by quality score descending
            valid_results = [r for r in results if r["quality_score"] > 0]
            if valid_results:
                best_email = sorted(valid_results, key=lambda x: x["quality_score"], reverse=True)[0]
            else:
                # If all are quality_score = 0, select first invalid
                best_email = results[0]
                
        success = best_email is not None and best_email["quality_score"] > 0
        
        # Step 3: Write results to DB and update lead status in a single atomic transaction
        async with db_manager.session_factory() as session:
            async with session.begin():
                lead_stmt = select(SearchLead).where(SearchLead.id == lead_id)
                lead_result = await session.execute(lead_stmt)
                db_lead = lead_result.scalars().first()
                
                validated_stmt = select(ValidatedEmail).where(ValidatedEmail.lead_id == lead_id)
                val_result = await session.execute(validated_stmt)
                existing_validation = val_result.scalars().first()
                
                # Succeeded lead status: EXTRACTED -> VALIDATED
                # Failed lead status: INVALID_EMAIL
                if db_lead:
                    db_lead.status = "VALIDATED" if success else "INVALID_EMAIL"
                    
                if best_email:
                    if existing_validation:
                        logger.warning(f"Validation record for lead {lead_id} already exists. Updating existing record...")
                        existing_validation.email = best_email["email"]
                        existing_validation.quality_score = best_email["quality_score"]
                        existing_validation.classification = best_email["classification"]
                        existing_validation.mx_status = "active" if best_email["mx_valid"] else "inactive"
                        existing_validation.domain_status = "resolved" if best_email["dns_valid"] else "unresolved"
                        existing_validation.disposable = best_email["disposable"]
                        existing_validation.role_based = best_email["role_based"]
                        existing_validation.confidence = best_email["confidence"]
                        existing_validation.recommended_action = best_email["recommended_action"]
                        existing_validation.validated_at = datetime.now(timezone.utc)
                    else:
                        new_val = ValidatedEmail(
                            lead_id=lead_id,
                            email=best_email["email"],
                            quality_score=best_email["quality_score"],
                            classification=best_email["classification"],
                            mx_status="active" if best_email["mx_valid"] else "inactive",
                            domain_status="resolved" if best_email["dns_valid"] else "unresolved",
                            disposable=best_email["disposable"],
                            role_based=best_email["role_based"],
                            confidence=best_email["confidence"],
                            recommended_action=best_email["recommended_action"]
                        )
                        session.add(new_val)
                        
            await session.commit()
            
        # Step 4: Downstream actions
        event_payload = {
            "lead_id": lead_id,
            "domain": url,
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
        
        if best_email:
            event_payload.update(best_email)
            
        if success:
            logger.info(f"Database update complete for lead {lead_id}. Status updated to VALIDATED. Quality Score: {best_email['quality_score']}")
            
            # Push lead to Redis downstream queue
            try:
                await redis_manager.push_to_queue(self.output_queue_name, url)
            except Exception as e:
                logger.warning(f"Queue: Failed to push to Redis downstream queue '{self.output_queue_name}': {e}")
        else:
            logger.warning(f"Database update complete for lead {lead_id}. Status updated to INVALID_EMAIL.")
            
        # Dispatch completion payload to Event Bus
        await event_bus.publish("email_validated", event_payload)
        
        return event_payload
