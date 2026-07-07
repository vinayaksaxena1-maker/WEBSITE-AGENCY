import os

class PreviewMetadata:
    @staticmethod
    def compile_metadata(image_path: str) -> dict:
        """
        Gathers image metadata parameters.
        """
        if not os.path.exists(image_path):
            return {}
            
        size = os.path.getsize(image_path)
        return {
            "format": "PNG",
            "file_size": size,
            "path": image_path
        }
