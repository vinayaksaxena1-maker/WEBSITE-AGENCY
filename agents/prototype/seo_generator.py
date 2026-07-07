from typing import Dict, Any

class SEOGenerator:
    @staticmethod
    def inject_seo_tags(html_content: str, metadata: Dict[str, Any]) -> str:
        """
        Embeds title headers and meta description parameters inside HTML head wrappers.
        """
        title = metadata.get("heading_text", "Enterprise Business Upgraded")
        desc = metadata.get("body_text", "Explore our optimized enterprise prototype offerings.")

        seo_block = f"""
        <title>{title}</title>
        <meta name="description" content="{desc}" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://agency-upgraded.com" />
        """

        if "</head>" in html_content:
            return html_content.replace("</head>", f"{seo_block}\n</head>")

        return html_content + seo_block
