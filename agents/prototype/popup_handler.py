import asyncio
from core.logger import logger

class PopupHandler:
    def __init__(self):
        # List of common selectors for overlays and cookie accept buttons
        self.popup_selectors = [
            # Cookie accept selectors
            "button:has-text('Accept')", "button:has-text('Agree')", "button:has-text('Allow')",
            "button:has-text('Accept All')", "button:has-text('I Agree')",
            "[id*='cookie-accept']", "[id*='cookie_accept']", "[class*='cookie-accept']",
            "[id*='accept-cookies']", "[class*='accept-cookies']",
            
            # Dismiss/close selectors
            "[class*='popup-close']", "[id*='popup-close']", ".close-modal", ".modal-close",
            "button[aria-label='Close']", "button[aria-label='dismiss']",
            
            # Chat overlay selectors
            "[class*='chat-widget-close']", ".intercom-launcher-frame", ".hubspot-conversations-iframe"
        ]

    async def dismiss_popups(self, page) -> None:
        """
        Attempts to find and close typical cookie banners, modal overlays, and chat widgets.
        Bypasses failures gracefully with log warnings.
        """
        logger.info("PopupHandler: Analyzing page for standard overlays and popups...")
        
        for selector in self.popup_selectors:
            try:
                # Use a small wait timeout to prevent blocking page loads
                element = await page.wait_for_selector(selector, timeout=100)
                if element and await element.is_visible():
                    await element.click()
                    logger.info(f"PopupHandler: Closed popup using selector: '{selector}'")
                    await asyncio.sleep(0.1)  # brief pause after clicking
            except Exception:
                # Silent skip if overlay not found or not clickable
                pass
        
        logger.info("PopupHandler: Overlay processing complete.")
