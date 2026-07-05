import asyncio
from core.logger import logger

class ScrollEngine:
    def __init__(self, step_px: int = 250, delay_ms: int = 100, max_scrolls: int = 50):
        self.step_px = step_px
        self.delay_ms = delay_ms
        self.max_scrolls = max_scrolls

    async def scroll_to_bottom_and_restore(self, page) -> None:
        """
        Incrementally scrolls the page down to trigger lazy loading,
        protecting against infinite-scrolling traps, then restores scroll to top.
        """
        logger.info("ScrollEngine: Starting incremental scroll execution...")
        
        try:
            # Inject JS to incrementally scroll the page
            await page.evaluate(f"""
                async () => {{
                    const step = {self.step_px};
                    const delay = {self.delay_ms};
                    const maxScrolls = {self.max_scrolls};
                    
                    let lastScrollTop = -1;
                    let scrollsCount = 0;
                    
                    while (scrollsCount < maxScrolls) {{
                        window.scrollBy(0, step);
                        await new Promise(resolve => setTimeout(resolve, delay));
                        
                        let currentScrollTop = window.scrollY;
                        if (currentScrollTop === lastScrollTop) {{
                            // Bottom of page reached
                            break;
                        }}
                        lastScrollTop = currentScrollTop;
                        scrollsCount++;
                    }}
                }}
            """)
            logger.info("ScrollEngine: Incremental scroll completed. Returning to page top...")
            # Restore to top for screenshotting
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(0.2)  # Wait briefly for rendering after scroll-to-top
        except Exception as e:
            logger.warning(f"ScrollEngine: Warning during scroll loop execution: {e}")
            # Ensure top restoration fallback
            try:
                await page.evaluate("window.scrollTo(0, 0)")
            except Exception:
                pass
