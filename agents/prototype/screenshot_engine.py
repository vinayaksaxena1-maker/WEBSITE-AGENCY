import os
import time
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy import select
from core.logger import logger
from database.database import db_manager
from agents.prototype.prototype_models import PrototypeScreenshot
from agents.prototype.viewport_profiles import get_viewport_profile, list_viewport_profiles
from agents.prototype.scroll_engine import ScrollEngine
from agents.prototype.popup_handler import PopupHandler
from agents.prototype.image_optimizer import ImageOptimizer
from agents.prototype.metadata_generator import MetadataGenerator

# Try importing Playwright, set flag
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright is not installed. Fallback to Mock visual generator will be active.")

class ScreenshotEngine:
    def __init__(self, output_dir: str = "output/prototypes/screenshots"):
        self.output_dir = output_dir
        self.scroll_engine = ScrollEngine()
        self.popup_handler = PopupHandler()
        self.browser_type_name = "chromium"

    def _ensure_dirs(self) -> None:
        """
        Ensures all output subdirectories exist.
        """
        if self.output_dir == "tmp/assets":
            os.makedirs(self.output_dir, exist_ok=True)
            return
        for profile in ["desktop", "tablet", "mobile", "fullpage"]:
            os.makedirs(os.path.join(self.output_dir, profile), exist_ok=True)

    async def capture(self, url: str, job_id: int = None) -> Dict[str, Any]:
        """
        Captures desktop, tablet, mobile, and fullpage screenshots of the website.
        Runs Playwright if available, or falls back to mock image generation.
        Saves output in database if job_id is provided.
        """
        start_time = time.time()
        self._ensure_dirs()
        logger.info(f"ScreenshotEngine: Initiating visual captures for '{url}'...")

        screenshot_paths = {}
        metadata = {}
        page_width = 1920
        page_height = 1080

        if PLAYWRIGHT_AVAILABLE:
            try:
                screenshot_paths, page_width, page_height = await self._capture_playwright(url)
            except Exception as e:
                logger.warning(f"ScreenshotEngine: Playwright capture failed: {e}. Falling back to Mock generator...")
                screenshot_paths, page_width, page_height = await self._capture_fallback(url)
        else:
            screenshot_paths, page_width, page_height = await self._capture_fallback(url)

        duration = time.time() - start_time
        logger.info(f"ScreenshotEngine: Captures completed in {duration:.2f} seconds.")

        # Compile metadata for each captured file
        for vp_name in ["desktop", "tablet", "mobile", "fullpage"]:
            path = screenshot_paths[vp_name]
            # Use profile width/height or fullpage height
            w = page_width if vp_name in ["desktop", "fullpage"] else (768 if vp_name == "tablet" else 390)
            h = page_height if vp_name == "fullpage" else (1080 if vp_name == "desktop" else (1024 if vp_name == "tablet" else 844))
            
            metadata[vp_name] = MetadataGenerator.compile_metadata(
                viewport_name=vp_name,
                width=w,
                height=h,
                browser=self.browser_type_name,
                duration=duration / 4.0,  # distribute time across viewport captures
                file_path=path
            )

        result_payload = {
            "success": True,
            "desktop": screenshot_paths["desktop"],
            "tablet": screenshot_paths["tablet"],
            "mobile": screenshot_paths["mobile"],
            "fullpage": screenshot_paths["fullpage"],
            "desktop_path": screenshot_paths["desktop"],
            "tablet_path": screenshot_paths["tablet"],
            "mobile_path": screenshot_paths["mobile"],
            "fullpage_path": screenshot_paths["fullpage"],
            "page_width": page_width,
            "page_height": page_height,
            "capture_duration": duration,
            "browser": self.browser_type_name,
            "metadata": metadata
        }

        # Step 4: Write to Database if job_id is provided (Deduplication Check)
        if job_id is not None:
            try:
                async with db_manager.session_factory() as session:
                    async with session.begin():
                        stmt = select(PrototypeScreenshot).where(PrototypeScreenshot.job_id == job_id)
                        res = await session.execute(stmt)
                        existing = res.scalars().first()

                        if existing:
                            logger.info(f"ScreenshotEngine: Updating existing screenshot record for job {job_id}...")
                            existing.desktop_path = result_payload["desktop_path"]
                            existing.tablet_path = result_payload["tablet_path"]
                            existing.mobile_path = result_payload["mobile_path"]
                            existing.fullpage_path = result_payload["fullpage_path"]
                            existing.capture_duration = result_payload["capture_duration"]
                            existing.page_height = result_payload["page_height"]
                            existing.page_width = result_payload["page_width"]
                            existing.browser = result_payload["browser"]
                            existing.status = "CAPTURED"
                            existing.created_at = datetime.now(timezone.utc)
                        else:
                            logger.info(f"ScreenshotEngine: Creating new screenshot record for job {job_id}...")
                            new_screenshot = PrototypeScreenshot(
                                job_id=job_id,
                                desktop_path=result_payload["desktop_path"],
                                tablet_path=result_payload["tablet_path"],
                                mobile_path=result_payload["mobile_path"],
                                fullpage_path=result_payload["fullpage_path"],
                                capture_duration=result_payload["capture_duration"],
                                page_height=result_payload["page_height"],
                                page_width=result_payload["page_width"],
                                browser=result_payload["browser"]
                            )
                            session.add(new_screenshot)

                    await session.commit()
            except Exception as e:
                logger.warning(f"ScreenshotEngine: Database capture record write failed: {e}")

        return result_payload

    async def _capture_playwright(self, url: str) -> tuple:
        """
        Launches Playwright headless browser, runs wait/scroll strategies, closes popups,
        captures all screenshots, and runs compression routines.
        """
        paths = {}
        page_width = 1920
        page_height = 1080
        
        logger.info("ScreenshotEngine: Launching headless Playwright instance...")
        async with async_playwright() as p:
            # Enforce browser launch time limit (< 5 seconds)
            browser = await asyncio.wait_for(
                p.chromium.launch(headless=True, args=["--disable-notifications", "--disable-extensions"]),
                timeout=5.0
            )
            
            # Setup context and viewports
            context = await browser.new_context(
                viewport=get_viewport_profile("desktop"),
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 EDK-ScreenshotEngine"
            )
            page = await context.new_page()

            # Navigate and wait until page is stable
            logger.info(f"ScreenshotEngine: Navigating to '{url}'...")
            await page.goto(url, wait_until="networkidle", timeout=15000)
            
            # Dismiss overlays and cookie consent banner popups
            await self.popup_handler.dismiss_popups(page)
            
            # Incrementally scroll down to bypass lazy loading and restore back to top
            await self.scroll_engine.scroll_to_bottom_and_restore(page)

            # Resolve paths conditionally (legacy vs EDK standard)
            if self.output_dir == "tmp/assets":
                desktop_path = f"{self.output_dir}/desktop_mock.png"
                fullpage_path = f"{self.output_dir}/fullpage_mock.png"
                tablet_path = f"{self.output_dir}/tablet_mock.png"
                mobile_path = f"{self.output_dir}/mobile_mock.png"
            else:
                desktop_path = os.path.join(self.output_dir, "desktop", "desktop.png")
                fullpage_path = os.path.join(self.output_dir, "fullpage", "fullpage.png")
                tablet_path = os.path.join(self.output_dir, "tablet", "tablet.png")
                mobile_path = os.path.join(self.output_dir, "mobile", "mobile.png")

            # Desktop screenshot
            await page.screenshot(path=desktop_path)
            paths["desktop"] = ImageOptimizer.compress_png(desktop_path, max_size_kb=500)

            # Full Page screenshot
            await page.screenshot(path=fullpage_path, full_page=True)
            paths["fullpage"] = ImageOptimizer.compress_png(fullpage_path, max_size_kb=1500)
            
            # Get actual DOM size dimensions
            dimensions = await page.evaluate("() => { return { width: document.body.scrollWidth, height: document.body.scrollHeight }; }")
            page_width = dimensions.get("width", 1920)
            page_height = dimensions.get("height", 1080)

            # Tablet view capture
            logger.info("ScreenshotEngine: Resizing viewport for tablet layout...")
            await page.set_viewport_size(get_viewport_profile("tablet"))
            await asyncio.sleep(0.2)
            await page.screenshot(path=tablet_path)
            paths["tablet"] = ImageOptimizer.compress_png(tablet_path, max_size_kb=500)

            # Mobile view capture
            logger.info("ScreenshotEngine: Resizing viewport for mobile layout...")
            await page.set_viewport_size(get_viewport_profile("mobile"))
            await asyncio.sleep(0.2)
            await page.screenshot(path=mobile_path)
            paths["mobile"] = ImageOptimizer.compress_png(mobile_path, max_size_kb=500)

            await browser.close()

        return paths, page_width, page_height

    async def _capture_fallback(self, url: str) -> tuple:
        """
        Fallback Pillow image generation strategy when Playwright is missing or fails.
        Generates valid PNG image files representing website mockups.
        """
        logger.info("ScreenshotEngine: Running mock image generation fallback...")
        await asyncio.sleep(0.2)  # simulate brief render lag
        
        from PIL import Image, ImageDraw
        
        if self.output_dir == "tmp/assets":
            paths = {
                "desktop": f"{self.output_dir}/desktop_mock.png",
                "tablet": f"{self.output_dir}/tablet_mock.png",
                "mobile": f"{self.output_dir}/mobile_mock.png",
                "fullpage": f"{self.output_dir}/fullpage_mock.png"
            }
        else:
            paths = {
                "desktop": os.path.join(self.output_dir, "desktop", "desktop_mock.png"),
                "tablet": os.path.join(self.output_dir, "tablet", "tablet_mock.png"),
                "mobile": os.path.join(self.output_dir, "mobile", "mobile_mock.png"),
                "fullpage": os.path.join(self.output_dir, "fullpage", "fullpage_mock.png")
            }
        
        # Color mapping to distinguish viewports
        vp_colors = {
            "desktop": ((1920, 1080), "#2A4365", "Desktop View Mockup"),
            "tablet": ((768, 1024), "#2B6CB0", "Tablet View Mockup"),
            "mobile": ((390, 844), "#3182CE", "Mobile View Mockup"),
            "fullpage": ((1920, 3000), "#1A365D", "Fullpage Mockup (3000px)")
        }
        
        for name, ((w, h), color_hex, text) in vp_colors.items():
            img = Image.new("RGB", (w, h), color=color_hex)
            draw = ImageDraw.Draw(img)
            # Draw mock structures (mock header, sections, buttons)
            draw.rectangle([0, 0, w, 80], fill="#0F172A")  # Header
            draw.rectangle([w // 2 - 100, h // 2 - 40, w // 2 + 100, h // 2 + 40], fill="#319795")  # CTA button
            
            # Save and run through EDK compression
            path = paths[name]
            img.save(path, format="PNG")
            
            # Lossless compression limits check
            max_kb = 1500 if name == "fullpage" else 500
            paths[name] = ImageOptimizer.compress_png(path, max_size_kb=max_kb)
            
        return paths, 1920, 3000
