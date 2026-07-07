class VersionManager:
    @staticmethod
    def get_next_version(current_version: str = "1.0.0", release_type: str = "patch") -> str:
        """
        Increments build SemVer version numbers.
        """
        parts = current_version.split(".")
        if len(parts) != 3:
            return "1.0.0"
            
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if release_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif release_type == "minor":
            minor += 1
            patch = 0
        else:
            patch += 1
            
        return f"{major}.{minor}.{patch}"
