import os
import zipfile
from core.logger import logger

class PackageBuilder:
    @staticmethod
    def create_zip(source_dir: str, output_zip_path: str) -> int:
        """
        Zips all files in the source directory and returns the package size in bytes.
        """
        logger.info(f"PackageBuilder: Bundling export package from {source_dir} to {output_zip_path}")
        
        os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)
        
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    
        size = os.path.getsize(output_zip_path)
        logger.info(f"PackageBuilder: Wrote ZIP package of size {size} bytes.")
        return size
