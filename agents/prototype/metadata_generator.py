import os
import time
from typing import Dict, Any
from core.logger import logger

class MetadataGenerator:
    @staticmethod
    def compile_metadata(
        viewport_name: str,
        width: int,
        height: int,
        browser: str,
        duration: float,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Compiles EDK-compliant screenshot capture metadata.
        """
        file_size_bytes = 0
        if os.path.exists(file_path):
            file_size_bytes = os.path.getsize(file_path)

        metadata = {
            "viewport_profile": viewport_name,
            "width": width,
            "height": height,
            "browser": browser,
            "capture_duration_seconds": round(duration, 3),
            "file_size_bytes": file_size_bytes,
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        logger.info(f"MetadataGenerator: Compiled metadata for '{viewport_name}' screenshot.")
        return metadata
