from typing import Dict, Any

COMPONENTS_LIBRARY: Dict[str, Dict[str, Any]] = {
    "HeaderComponent": {
        "name": "HeaderComponent",
        "priority": "Critical",
        "dependencies": ["NavigationComponent"],
        "default_variant": "modern",
        "description": "Standard top navigation bar header."
    },
    "NavigationComponent": {
        "name": "NavigationComponent",
        "priority": "Critical",
        "dependencies": [],
        "default_variant": "modern",
        "description": "Desktop mega menu and mobile hamburger navigation list."
    },
    "HeroComponent": {
        "name": "HeroComponent",
        "priority": "Critical",
        "dependencies": ["ButtonComponent"],
        "default_variant": "modern",
        "description": "Opening banner containing primary marketing headlines and CTA buttons."
    },
    "ServicesComponent": {
        "name": "ServicesComponent",
        "priority": "High",
        "dependencies": ["CardComponent"],
        "default_variant": "modern",
        "description": "Grids section listing services features offerings."
    },
    "FAQComponent": {
        "name": "FAQComponent",
        "priority": "Medium",
        "dependencies": ["AccordionComponent"],
        "default_variant": "modern",
        "description": "Accordions list answering frequently asked questions."
    },
    "TestimonialsComponent": {
        "name": "TestimonialsComponent",
        "priority": "High",
        "dependencies": ["CardComponent"],
        "default_variant": "modern",
        "description": "Reviews list showing customer feedback."
    },
    "ContactFormComponent": {
        "name": "ContactFormComponent",
        "priority": "High",
        "dependencies": ["ButtonComponent"],
        "default_variant": "modern",
        "description": "Contact form panel with fields, textarea, and submit button."
    },
    "FooterComponent": {
        "name": "FooterComponent",
        "priority": "Critical",
        "dependencies": ["NavigationComponent"],
        "default_variant": "modern",
        "description": "Footer section showing copyrights and secondary links."
    },
    "CardComponent": {
        "name": "CardComponent",
        "priority": "Low",
        "dependencies": [],
        "default_variant": "modern",
        "description": "Standard content wrapper card with image and description."
    },
    "AccordionComponent": {
        "name": "AccordionComponent",
        "priority": "Low",
        "dependencies": [],
        "default_variant": "modern",
        "description": "Standard collapsible accordion wrapper."
    },
    "ButtonComponent": {
        "name": "ButtonComponent",
        "priority": "Low",
        "dependencies": [],
        "default_variant": "modern",
        "description": "Interactive action button trigger."
    },
    "SectionComponent": {
        "name": "SectionComponent",
        "priority": "Medium",
        "dependencies": [],
        "default_variant": "modern",
        "description": "Generic layout fallback section."
    }
}
