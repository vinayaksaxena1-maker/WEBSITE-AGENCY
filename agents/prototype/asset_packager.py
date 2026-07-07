import os
import shutil
from core.logger import logger

class AssetPackager:
    @staticmethod
    def collect_assets(html_path: str, css_path: str, dest_dir: str) -> int:
        """
        Copies assets into destination folder structure.
        """
        logger.info(f"AssetPackager: Copying assets to destination {dest_dir}")
        count = 0
        
        # Copy index HTML
        if os.path.exists(html_path):
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copyfile(html_path, os.path.join(dest_dir, "index.html"))
            count += 1
            
        # Copy CSS
        css_dest_dir = os.path.join(dest_dir, "assets", "css")
        os.makedirs(css_dest_dir, exist_ok=True)
        if os.path.exists(css_path):
            shutil.copyfile(css_path, os.path.join(css_dest_dir, "mock_prototype.css"))
            count += 1
            
        return count
