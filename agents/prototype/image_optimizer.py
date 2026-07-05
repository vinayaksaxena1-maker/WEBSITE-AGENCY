import os
from PIL import Image
from core.logger import logger

class ImageOptimizer:
    @staticmethod
    def compress_png(input_path: str, max_size_kb: int = 1500) -> str:
        """
        Compresses input PNG losslessly, aligning to sRGB, and checks file bounds.
        """
        if not os.path.exists(input_path):
            logger.error(f"ImageOptimizer: File not found at '{input_path}'")
            return input_path

        logger.info(f"ImageOptimizer: Optimizing PNG file '{input_path}'...")
        
        try:
            with Image.open(input_path) as img:
                # Align to RGB/sRGB colorspace if necessary
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")
                
                # Save losslessly with optimization and highest compression level (9)
                img.save(
                    input_path,
                    format="PNG",
                    optimize=True,
                    compress_level=9
                )

            # Validate size limits
            file_size_kb = os.path.getsize(input_path) / 1024.0
            logger.info(f"ImageOptimizer: Compression completed. New size: {file_size_kb:.2f} KB (Target: <{max_size_kb} KB)")
            
            if file_size_kb > max_size_kb:
                logger.warning(
                    f"ImageOptimizer: File size ({file_size_kb:.2f} KB) exceeds the targeted limit of {max_size_kb} KB."
                )
            
            return input_path
        except Exception as e:
            logger.warning(f"ImageOptimizer: Failed to compress image '{input_path}': {e}")
            return input_path
