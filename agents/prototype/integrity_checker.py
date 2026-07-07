import os
import zipfile
from core.logger import logger

class IntegrityChecker:
    @staticmethod
    def verify_zip_integrity(zip_path: str) -> bool:
        """
        Tests ZIP archive to ensure there are no corrupted bits.
        """
        logger.info(f"IntegrityChecker: Verifying ZIP integrity for {zip_path}")
        if not os.path.exists(zip_path):
            return False
            
        try:
            with zipfile.ZipFile(zip_path, "r") as zipf:
                # testzip returns None if zip is valid, otherwise returns first bad file
                bad_file = zipf.testzip()
                if bad_file is not None:
                    logger.warning(f"IntegrityChecker: ZIP corrupted at file {bad_file}")
                    return False
            return True
        except Exception as e:
            logger.warning(f"IntegrityChecker: Integrity test failed: {e}")
            return False
