import json
from typing import Dict, Any

class SchemaGenerator:
    @staticmethod
    def get_organization_schema(metadata: Dict[str, Any]) -> str:
        """
        Builds JSON-LD Organization schema structures.
        """
        title = metadata.get("heading_text", "Enterprise Business Upgraded")
        addr = metadata.get("address", "Available upon request")
        
        schema_dict = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": title,
            "url": "https://agency-upgraded.com",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": addr
            }
        }

        schema_json = json.dumps(schema_dict, indent=2)
        return f'<script type="application/ld+json">\n{schema_json}\n</script>'

    @classmethod
    def inject_schema(cls, html_content: str, metadata: Dict[str, Any]) -> str:
        schema_block = cls.get_organization_schema(metadata)
        if "</head>" in html_content:
            return html_content.replace("</head>", f"{schema_block}\n</head>")
        return html_content + schema_block
