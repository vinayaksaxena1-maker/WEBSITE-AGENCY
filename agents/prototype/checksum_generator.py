import hashlib

class ChecksumGenerator:
    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        """
        Calculates SHA-256 checksum for the file.
        """
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception:
            return ""
