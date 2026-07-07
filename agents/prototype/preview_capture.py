import os
from PIL import Image, ImageDraw
from core.logger import logger

class PreviewCapture:
    @staticmethod
    def capture_screenshot(url: str, output_path: str, width: int, height: int) -> bool:
        """
        Captures mockup preview screenshots, falling back to PIL drawings on environments missing crawlers.
        """
        logger.info(f"PreviewCapture: Simulating screenshot capture from {url} on viewport {width}x{height}")
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Create a mock screenshot matching viewport size
            img = Image.new("RGB", (width, height), color="#0F172A")
            draw = ImageDraw.Draw(img)
            
            # Simple design block drawing
            draw.rectangle([20, 20, width-20, height-20], outline="#3B82F6", width=4)
            draw.text((40, 40), f"Mock Preview Viewport: {width}x{height}", fill="#FFFFFF")
            draw.text((40, 80), f"Loaded: {url}", fill="#94A3B8")

            img.save(output_path)
            return True
        except Exception as e:
            logger.warning(f"PreviewCapture: Screenshot writing failed: {e}")
            return False
