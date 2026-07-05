from abc import ABC, abstractmethod
from typing import Dict, Any

class IContactAgent(ABC):
    @abstractmethod
    async def extract_contacts(self, lead_id: int, url: str) -> Dict[str, Any]:
        """
        Main orchestration entry point:
        1. Checks lead status in database.
        2. Retrieves home page content.
        3. Parses internal subpage links (about, contact, etc.).
        4. Fetches and processes subpages in parallel.
        5. Normalizes and validates extracted contacts.
        6. Saves/updates contacts in database.
        7. Updates lead status (EXTRACTED or NO_CONTACT).
        8. Pushes lead URL to downstream validation_queue.
        9. Publishes 'contact_extracted' event to Event Bus.
        """
        pass
