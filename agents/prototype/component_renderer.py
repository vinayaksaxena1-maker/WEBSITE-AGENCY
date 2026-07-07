from typing import Dict, Any, List
from core.logger import logger

BOILERPLATES = {
    "header": """
    <header class="w-full py-4 px-6 border-b border-gray-100 flex items-center justify-between bg-white text-gray-900">
        <div class="text-xl font-bold flex items-center gap-2">Logo</div>
        <nav class="hidden md:flex items-center gap-6 text-sm font-medium">
            <a href="#" class="hover:text-primary transition-colors">Home</a>
            <a href="#" class="hover:text-primary transition-colors">Services</a>
            <a href="#" class="hover:text-primary transition-colors">Contact</a>
        </nav>
    </header>
    """,
    "hero": """
    <section class="py-20 px-8 text-center bg-gray-50 text-gray-900">
        <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight mb-4">[[heading_text]]</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto mb-8">[[body_text]]</p>
        <button class="px-8 py-3 bg-primary text-white font-semibold rounded-lg shadow-md hover:bg-opacity-90 transition-all">Get Started</button>
    </section>
    """,
    "services": """
    <section class="py-16 px-8 bg-white text-gray-900">
        <h2 class="text-3xl font-bold text-center mb-12">Our Services</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div class="p-6 border rounded-xl shadow-sm hover:shadow-md transition-shadow">
                <h3 class="text-xl font-semibold mb-2">Service Alpha</h3>
                <p class="text-sm text-gray-600">High quality enterprise level support offerings.</p>
            </div>
            <div class="p-6 border rounded-xl shadow-sm hover:shadow-md transition-shadow">
                <h3 class="text-xl font-semibold mb-2">Service Beta</h3>
                <p class="text-sm text-gray-600">Advanced custom workflow integrations features.</p>
            </div>
            <div class="p-6 border rounded-xl shadow-sm hover:shadow-md transition-shadow">
                <h3 class="text-xl font-semibold mb-2">Service Gamma</h3>
                <p class="text-sm text-gray-600">Comprehensive scaling strategies optimization.</p>
            </div>
        </div>
    </section>
    """,
    "footer": """
    <footer class="w-full py-8 px-6 bg-gray-900 text-gray-400 text-center text-sm border-t border-gray-800">
        <div class="mb-4">&copy; 2026 Enterprise Agency. All rights reserved.</div>
        <div class="flex justify-center gap-6">
            <a href="#" class="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#" class="hover:text-white transition-colors">Terms of Service</a>
        </div>
    </footer>
    """
}

class ComponentRenderer:
    @staticmethod
    def render_layout(structure: List[Dict[str, Any]], heading: str, body: str) -> str:
        """
        Loops through structure, matches tags to templates, and replaces content tokens.
        """
        logger.info("ComponentRenderer: Compiling layout structural blocks...")
        html_blocks = []

        for item in structure:
            sec_name = item.get("type", "services").lower()
            
            # Fuzzy match presets key
            template = ""
            for k, val in BOILERPLATES.items():
                if k in sec_name:
                    template = val
                    break
            
            if not template:
                template = BOILERPLATES["services"]  # fallback default block

            # Interpolate parameters
            block = template.replace("[[heading_text]]", heading).replace("[[body_text]]", body)
            html_blocks.append(block)

        return "\n".join(html_blocks)
