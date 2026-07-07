from typing import Dict, Any

class TailwindGenerator:
    @staticmethod
    def get_root_styles(theme: Dict[str, Any]) -> str:
        """
        Generates CSS root variable styling tokens using theme colors.
        """
        p = theme.get("primary_color", "#1E3A8A")
        s = theme.get("secondary_color", "#3B82F6")
        a = theme.get("accent_color", "#F59E0B")
        bg = theme.get("background_color", "#FFFFFF")
        txt = theme.get("text_color", "#0F172A")

        return f"""
        :root {{
            --primary: {p};
            --secondary: {s};
            --accent: {a};
            --background: {bg};
            --text: {txt};
        }}
        .text-primary {{ color: var(--primary); }}
        .bg-primary {{ background-color: var(--primary); }}
        .border-primary {{ border-color: var(--primary); }}
        """
