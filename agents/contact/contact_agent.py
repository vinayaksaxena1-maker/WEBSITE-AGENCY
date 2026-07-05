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
from agents.contact.contact_parser import ContactParser
from agents.audit.browser_engine import UrllibBrowserEngine
from agents.contact.interfaces import IContactAgent

class ContactAgent(IContactAgent):
    def __init__(self, browser_engine = None, parser = None):
        self.browser_engine = browser_engine or UrllibBrowserEngine()
        self.parser = parser or ContactParser()
        self.output_queue_name = "validation_queue"

    async def crawl_and_parse(self, url: str) -> Dict[str, Any]:
        """
        Crawls the homepage and internal subpages, extracting all contact details.
        """
        logger.info(f"Crawl: Fetching homepage '{url}'...")
        home_data = await self.browser_engine.fetch_url(url, timeout=4.0)
        home_html = home_data.get("html", "")
        
        pages_content = {url: home_html}
        
        # Extract and limit internal target links (max 5 to avoid overloading)
        subpage_urls = self.parser.extract_internal_links(home_html, url)[:5]
        
        if subpage_urls:
            logger.info(f"Crawl: Found {len(subpage_urls)} internal target subpages. Fetching concurrently...")
            async def fetch_subpage(sub_url: str):
                try:
                    data = await self.browser_engine.fetch_url(sub_url, timeout=3.0)
                    return sub_url, data.get("html", "")
                except Exception as e:
                    logger.warning(f"Crawl: Failed to fetch subpage '{sub_url}': {e}")
                    return sub_url, ""
            
            tasks = [fetch_subpage(sub_url) for sub_url in subpage_urls]
            results = await asyncio.gather(*tasks)
            for sub_url, html in results:
                if html:
                    pages_content[sub_url] = html
                    
        return self.parser.parse_site_data(pages_content, url)

    async def extract_contacts(self, lead_id: int, url: str) -> Dict[str, Any]:
        logger.info(f"Starting Contact Extraction pipeline for lead {lead_id} ('{url}')...")
        
        # Step 1: Verify lead existence
        async with db_manager.session_factory() as session:
            stmt = select(SearchLead).where(SearchLead.id == lead_id)
            result = await session.execute(stmt)
            lead = result.scalars().first()
            
            if not lead:
                logger.error(f"Lead ID {lead_id} not found in database search_leads table.")
                raise ValueError(f"Lead ID {lead_id} does not exist.")
                
        # Step 2: Crawl & parse website with a strict timeout (9.0 seconds to leave room for DB commits)
        success = False
        parsed_data = {}
        
        try:
            parsed_data = await asyncio.wait_for(self.crawl_and_parse(url), timeout=9.0)
            success = True
        except asyncio.TimeoutError:
            logger.error(f"Timeout: Contact extraction crawling for '{url}' timed out after 9.0s.")
        except Exception as e:
            logger.error(f"Failure: Contact extraction crawling for '{url}' failed: {e}", exc_info=True)
            
        # Step 3: Write results to DB and update lead status in a single atomic transaction
        async with db_manager.session_factory() as session:
            async with session.begin():
                # Re-fetch lead inside transaction scope to update status
                lead_stmt = select(SearchLead).where(SearchLead.id == lead_id)
                lead_result = await session.execute(lead_stmt)
                db_lead = lead_result.scalars().first()
                
                # Check for existing contact record to avoid unique constraints
                contact_stmt = select(Contact).where(Contact.lead_id == lead_id)
                contact_result = await session.execute(contact_stmt)
                existing_contact = contact_result.scalars().first()
                
                if success:
                    # Update status to EXTRACTED
                    if db_lead:
                        db_lead.status = "EXTRACTED"
                        
                    if existing_contact:
                        logger.warning(f"Contact for lead {lead_id} already exists. Updating existing record...")
                        existing_contact.primary_email = parsed_data.get("primary_email")
                        existing_contact.secondary_email = parsed_data.get("secondary_email")
                        existing_contact.phone = parsed_data.get("phone")
                        existing_contact.whatsapp = parsed_data.get("whatsapp")
                        existing_contact.facebook = parsed_data.get("facebook")
                        existing_contact.instagram = parsed_data.get("instagram")
                        existing_contact.linkedin = parsed_data.get("linkedin")
                        existing_contact.twitter = parsed_data.get("twitter")
                        existing_contact.youtube = parsed_data.get("youtube")
                        existing_contact.website = parsed_data.get("website")
                        existing_contact.status = parsed_data.get("status", "No Contact")
                        existing_contact.updated_at = datetime.now(timezone.utc)
                    else:
                        new_contact = Contact(
                            lead_id=lead_id,
                            primary_email=parsed_data.get("primary_email"),
                            secondary_email=parsed_data.get("secondary_email"),
                            phone=parsed_data.get("phone"),
                            whatsapp=parsed_data.get("whatsapp"),
                            facebook=parsed_data.get("facebook"),
                            instagram=parsed_data.get("instagram"),
                            linkedin=parsed_data.get("linkedin"),
                            twitter=parsed_data.get("twitter"),
                            youtube=parsed_data.get("youtube"),
                            website=parsed_data.get("website"),
                            status=parsed_data.get("status", "No Contact")
                        )
                        session.add(new_contact)
                else:
                    # Failed crawl: Update status to NO_CONTACT
                    if db_lead:
                        db_lead.status = "NO_CONTACT"
                        
            await session.commit()
            
        # Step 4: Downstream actions on success
        event_payload = {
            "lead_id": lead_id,
            "domain": url,
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
        
        if success:
            event_payload.update(parsed_data)
            logger.info(f"Database update complete for lead {lead_id}. Status updated to EXTRACTED. Contact status: {parsed_data.get('status')}")
            
            # Push lead to Redis downstream queue
            try:
                await redis_manager.push_to_queue(self.output_queue_name, url)
            except Exception as e:
                logger.warning(f"Queue: Failed to push to Redis downstream queue '{self.output_queue_name}': {e}")
        else:
            logger.warning(f"Database update complete for lead {lead_id}. Status updated to NO_CONTACT.")
            
        # Dispatch completion payload to Event Bus
        await event_bus.publish("contact_extracted", event_payload)
        
        return event_payload
