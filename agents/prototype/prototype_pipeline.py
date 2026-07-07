import time
from typing import Dict, Any
from core.logger import logger
from agents.prototype.browser_engine import BrowserEngine
from agents.prototype.screenshot_engine import ScreenshotEngine
from agents.prototype.dom_analyzer import DOMAnalyzer
from agents.prototype.visual_analyzer import VisualAnalyzer
from agents.prototype.theme_engine import ThemeEngine
from agents.prototype.layout_engine import LayoutEngine
from agents.prototype.component_engine import ComponentEngine
from agents.prototype.responsive_engine import ResponsiveEngine
from agents.prototype.html_generator import HTMLGenerator
from agents.prototype.preview_generator import PreviewGenerator
from agents.prototype.quality_analyzer import QualityAnalyzer

class PrototypePipeline:
    def __init__(self):
        self.browser = BrowserEngine()
        self.screenshot_engine = ScreenshotEngine()
        self.dom_analyzer = DOMAnalyzer()
        self.visual_analyzer = VisualAnalyzer()
        self.theme_engine = ThemeEngine()
        self.layout_engine = LayoutEngine()
        self.component_engine = ComponentEngine()
        self.responsive_engine = ResponsiveEngine()
        self.html_generator = HTMLGenerator()
        self.preview_generator = PreviewGenerator()
        self.quality_analyzer = QualityAnalyzer()

    async def execute_pipeline(self, url: str, category: str, job_id: int = None) -> Dict[str, Any]:
        """
        Coordinates the multi-stage Prototype Intelligence Engine pipeline.
        """
        start_time = time.time()
        logger.info(f"PrototypePipeline: Initiating generation pipeline for '{url}'...")

        try:
            # 1. Launch Browser
            await self.browser.launch()

            # 2. Open Page
            html_content = await self.browser.get_page(url)

            # 3. Capture Screenshots
            screenshots = await self.screenshot_engine.capture(url, job_id=job_id)

            # 4. DOM Analysis
            dom_data = await self.dom_analyzer.analyze(html_content, job_id=job_id)

            # 5. Visual Analysis
            visuals = await self.visual_analyzer.analyze_visuals(screenshots, html_content=html_content, job_id=job_id)

            # 6. Select Theme
            theme = await self.theme_engine.select_theme(category, visuals, job_id=job_id)

            # 7. Generate Layout Grid
            layout = await self.layout_engine.create_layout_grid(dom_data.get("sections", []), theme, job_id=job_id)

            # 8. Assemble Reusable Components
            raw_components = await self.component_engine.assemble_components(layout, theme=theme, job_id=job_id)

            # 9. Apply Responsive Viewport Overrides
            responsive_components = await self.responsive_engine.make_responsive(raw_components, job_id=job_id)

            # 10. Generate Output HTML / CSS Files
            files = await self.html_generator.generate(responsive_components, theme, job_id=job_id)

            # 11. Generate High-Res Preview snapshot
            preview_path = await self.preview_generator.generate_preview(files.get("html_path", ""), job_id=job_id)

            # 12. Evaluate Quality score
            quality = await self.quality_analyzer.analyze_quality(files.get("html_path", ""), files.get("css_path", ""), job_id=job_id)

            # Close browser context
            await self.browser.close()

            execution_time = time.time() - start_time
            logger.info(f"PrototypePipeline: Generation complete in {execution_time:.2f} seconds.")

            return {
                "success": True,
                "html_path": files.get("html_path"),
                "css_path": files.get("css_path"),
                "preview_path": preview_path,
                "theme_name": theme.get("name"),
                "quality_score": quality.get("quality_score", 0),
                "improvements": quality.get("improvements", []),
                "warnings": quality.get("warnings", []),
                "recommendations": quality.get("recommendations", []),
                "execution_time": execution_time,
                "assets": [
                    {"type": "desktop_screenshot", "path": screenshots.get("desktop")},
                    {"type": "tablet_screenshot", "path": screenshots.get("tablet")},
                    {"type": "mobile_screenshot", "path": screenshots.get("mobile")},
                    {"type": "full_page_screenshot", "path": screenshots.get("full_page")},
                    {"type": "preview_thumbnail", "path": preview_path}
                ]
            }

        except Exception as e:
            logger.error(f"PrototypePipeline: Critical pipeline failure: {e}", exc_info=True)
            # Safe browser cleanup
            try:
                await self.browser.close()
            except Exception:
                pass
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }
