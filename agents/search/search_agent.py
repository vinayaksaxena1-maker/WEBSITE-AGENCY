from typing import List, Dict, Any
from sqlalchemy.future import select
from core.logger import logger
from database.database import db_manager
from database.redis_manager import redis_manager
from agents.search.search_models import SearchLead
from agents.search.domain_filter import domain_filter
from agents.search.scraper_service import DuckDuckGoScraper, ISearchScraper

class SearchAgent:
    def __init__(self, scraper: ISearchScraper = None):
        self.scraper = scraper or DuckDuckGoScraper()
        self.queue_name = "audit_queue"

    async def execute(self, niche: str, geographic_target: str, limit: int = 50) -> Dict[str, Any]:
        logger.info(f"Starting Search Agent execution for niche '{niche}' in region '{geographic_target}'...")
        
        query = f"{niche} {geographic_target} website"
        raw_links = await self.scraper.search(query, limit=100)
        
        discovered_count = 0
        duplicates_count = 0
        blacklisted_count = 0
        stored_leads = []
        
        # Stage 1: Domain filter pipeline
        validated_domains = set()
        for link in raw_links:
            clean_domain = domain_filter.validate(link)
            if not clean_domain:
                blacklisted_count += 1
                continue
            validated_domains.add(clean_domain)
            
        logger.info(f"Filter stage: {len(validated_domains)} unique clean domains extracted.")
        
        # Stage 2: Database deduplication & transactional insertion
        async with db_manager.session_factory() as session:
            async with session.begin():
                for domain in validated_domains:
                    stmt = select(SearchLead).where(SearchLead.domain == domain)
                    result = await session.execute(stmt)
                    existing = result.scalars().first()
                    
                    if existing:
                        duplicates_count += 1
                        continue
                        
                    new_lead = SearchLead(
                        domain=domain,
                        niche=niche,
                        source="DuckDuckGoScraper",
                        status="DISCOVERED"
                    )
                    session.add(new_lead)
                    discovered_count += 1
                    stored_leads.append(domain)
                    
            await session.commit()
            
        # Stage 3: Push enqueues to Redis queue
        for domain in stored_leads:
            await redis_manager.push_to_queue(self.queue_name, domain)
            
        logger.info(f"Database update complete. Discovered: {discovered_count}, Duplicates: {duplicates_count}, Blacklisted: {blacklisted_count}")
        
        # Compile EDK-standardized Audit Report
        audit_report = {
            "status": "PASS" if (len(validated_domains) >= 50) else "FAIL",
            "niche": niche,
            "geographic_target": geographic_target,
            "total_links_parsed": len(raw_links),
            "validated_domains": len(validated_domains),
            "inserted_count": discovered_count,
            "duplicates_count": duplicates_count,
            "blacklisted_count": blacklisted_count,
            "stored_leads": stored_leads
        }
        
        return audit_report
