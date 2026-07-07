import os
from core.logger import logger

class AssetManager:
    @staticmethod
    def ensure_directories(base_dir: str) -> None:
        """
        Guarantees destination subfolders exist.
        """
        folders = [
            base_dir,
            os.path.join(base_dir, "assets"),
            os.path.join(base_dir, "assets", "css"),
            os.path.join(base_dir, "assets", "js"),
            os.path.join(base_dir, "assets", "images"),
            os.path.join(base_dir, "assets", "icons")
        ]
        
        for f in folders:
            if not os.path.exists(f):
                os.makedirs(f, exist_ok=True)
                logger.info(f"AssetManager: Created directory '{f}'")
