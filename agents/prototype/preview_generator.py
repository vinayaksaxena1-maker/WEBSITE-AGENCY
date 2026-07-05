import asyncio
from core.logger import logger

class PreviewGenerator:
    def __init__(self, output_dir: str = "output/prototypes/previews"):
        self.output_dir = output_dir

    async def generate_preview(self, html_path: str) -> str:
        """
        Loads the generated HTML in browser and captures a high-resolution preview.
        """
        logger.info(f"PreviewGenerator: Capturing mock PNG preview for '{html_path}' (mocked)...")
        await asyncio.sleep(0.1)
        
        return f"{self.output_dir}/mock_preview.png"
