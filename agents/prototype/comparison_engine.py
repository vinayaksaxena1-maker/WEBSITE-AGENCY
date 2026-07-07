import os
from PIL import Image, ImageDraw, ImageFont
from core.logger import logger

class ComparisonEngine:
    @staticmethod
    def compile_comparison(before_path: str, after_path: str, output_path: str) -> bool:
        """
        Creates side-by-side or combined Before/After rendering layouts comparison.
        """
        logger.info(f"ComparisonEngine: Compiling layout comparison from {before_path} and {after_path}")
        
        try:
            # Load images
            if os.path.exists(before_path):
                img_before = Image.open(before_path)
            else:
                img_before = Image.new("RGB", (640, 480), color="#1E3A8A")
                draw = ImageDraw.Draw(img_before)
                draw.text((50, 200), "Mock Before Target Screenshot", fill="#FFFFFF")

            if os.path.exists(after_path):
                img_after = Image.open(after_path)
            else:
                img_after = Image.new("RGB", (640, 480), color="#10B981")
                draw = ImageDraw.Draw(img_after)
                draw.text((50, 200), "Mock After Upgraded Template Rendering", fill="#FFFFFF")

            # Resize to match dimensions
            w, h = 640, 480
            img_before = img_before.resize((w, h))
            img_after = img_after.resize((w, h))

            # Combine side-by-side
            combined = Image.new("RGB", (w * 2, h))
            combined.paste(img_before, (0, 0))
            combined.paste(img_after, (w, 0))

            # Ensure output folder exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            combined.save(output_path)
            logger.info(f"ComparisonEngine: Wrote comparison image to {output_path}")
            return True
        except Exception as e:
            logger.warning(f"ComparisonEngine: Image composite building failed: {e}")
            return False
