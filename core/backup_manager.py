import shutil
import os
from datetime import datetime
from core.logger import logger

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = backup_dir

    def create_backup(self, filepath: str) -> bool:
        if not os.path.exists(filepath):
            logger.warning(f"Cannot backup file {filepath}; file does not exist.")
            return False
            
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            filename = os.path.basename(filepath)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"{filename}.{timestamp}.bak")
            
            shutil.copy2(filepath, backup_path)
            logger.info(f"Successfully created backup of '{filepath}' to '{backup_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error creating backup of '{filepath}': {e}", exc_info=True)
            return False

backup_manager = BackupManager()
