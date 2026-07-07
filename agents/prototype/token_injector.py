from typing import Dict, Any

class TokenInjector:
    @staticmethod
    def inject_tokens(html_content: str, css_styles: str) -> str:
        """
        Injects CSS styling tokens variables into HTML head tag block.
        """
        style_block = f"""
        <style>
        {css_styles}
        </style>
        """
        
        # Insert style block before </head> tag
        if "</head>" in html_content:
            return html_content.replace("</head>", f"{style_block}\n</head>")
            
        return html_content + style_block
