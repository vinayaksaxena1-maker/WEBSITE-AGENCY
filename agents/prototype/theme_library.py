from typing import Dict, Any

THEMES_CATALOG: Dict[str, Dict[str, Any]] = {
    "medical": {
        "name": "Medical Clear Trust Theme",
        "category": "Medical",
        "personality": "Clean / High Trust",
        "colors": {
            "primary": "#0F766E",      # Teal
            "secondary": "#0D9488",    # Teal Medium
            "accent": "#F59E0B",       # Gold
            "background": "#F0FDFA",   # Very Light Teal
            "surface": "#FFFFFF",
            "text": "#0F172A",
            "text_muted": "#475569"
        },
        "typography": {
            "heading": "Inter",
            "body": "Inter"
        }
    },
    "fitness": {
        "name": "Fitness Energetic Dark Theme",
        "category": "Bold Marketing",
        "personality": "Energetic / Bold",
        "colors": {
            "primary": "#EA580C",      # Orange
            "secondary": "#1E1B4B",    # Indigo dark
            "accent": "#F59E0B",       # Amber
            "background": "#0B0F19",   # Dark Slate
            "surface": "#1E293B",
            "text": "#F8FAFC",
            "text_muted": "#94A3B8"
        },
        "typography": {
            "heading": "Oswald",
            "body": "Roboto"
        }
    },
    "restaurant": {
        "name": "Warm Cozy Bistro Theme",
        "category": "Creative Studio",
        "personality": "Friendly / Cozy",
        "colors": {
            "primary": "#DC2626",      # Warm Red
            "secondary": "#F59E0B",    # Gold
            "accent": "#10B981",       # Emerald
            "background": "#FFFBEB",   # Warm Amber Light
            "surface": "#FFFFFF",
            "text": "#451A03",         # Warm Brown
            "text_muted": "#78350F"
        },
        "typography": {
            "heading": "Playfair Display",
            "body": "Lato"
        }
    },
    "law firm": {
        "name": "Law Firm Legacy Traditional Theme",
        "category": "Corporate Professional",
        "personality": "Traditional / Reliable",
        "colors": {
            "primary": "#1E3A8A",      # Navy Blue
            "secondary": "#475569",    # Slate Grey
            "accent": "#D97706",       # Bronze
            "background": "#F8FAFC",   # Slate Light
            "surface": "#FFFFFF",
            "text": "#0F172A",
            "text_muted": "#475569"
        },
        "typography": {
            "heading": "Merriweather",
            "body": "Open Sans"
        }
    },
    "technology": {
        "name": "Modern Cyberpunk Indigo Theme",
        "category": "Technology",
        "personality": "Innovative / Modern",
        "colors": {
            "primary": "#4F46E5",      # Indigo
            "secondary": "#7C3AED",    # Purple
            "accent": "#10B981",       # Accent Emerald
            "background": "#0F172A",   # Dark Slate
            "surface": "#1E293B",
            "text": "#F8FAFC",
            "text_muted": "#94A3B8"
        },
        "typography": {
            "heading": "Outfit",
            "body": "Inter"
        }
    },
    "fashion": {
        "name": "Elegant Luxury Charcoal Theme",
        "category": "Premium Luxury",
        "personality": "Minimal / Elegant",
        "colors": {
            "primary": "#111827",      # Deep Charcoal
            "secondary": "#6B7280",    # Cool Grey
            "accent": "#D97706",       # Bronze Gold
            "background": "#FAFAFA",   # Crisp White
            "surface": "#FFFFFF",
            "text": "#111827",
            "text_muted": "#4B5563"
        },
        "typography": {
            "heading": "Playfair Display",
            "body": "Montserrat"
        }
    },
    "default": {
        "name": "Modern Corporate Reliable Theme",
        "category": "Modern Business",
        "personality": "Reliable / Professional",
        "colors": {
            "primary": "#1E3A8A",      # Corporate Blue
            "secondary": "#3B82F6",    # Trust Blue
            "accent": "#F59E0B",       # Amber
            "background": "#FFFFFF",
            "surface": "#F8FAFC",
            "text": "#0F172A",
            "text_muted": "#64748B"
        },
        "typography": {
            "heading": "Inter",
            "body": "Inter"
        }
    }
}

def get_theme_preset(niche: str) -> Dict[str, Any]:
    niche_lower = niche.strip().lower()
    
    # Fuzzy match standard nicknames
    if "hospital" in niche_lower or "clinic" in niche_lower or "medical" in niche_lower or "healthcare" in niche_lower:
        return THEMES_CATALOG["medical"]
    elif "fitness" in niche_lower or "gym" in niche_lower or "sports" in niche_lower:
        return THEMES_CATALOG["fitness"]
    elif "restaurant" in niche_lower or "food" in niche_lower or "cafe" in niche_lower or "bistro" in niche_lower:
        return THEMES_CATALOG["restaurant"]
    elif "law" in niche_lower or "legal" in niche_lower or "attorney" in niche_lower:
        return THEMES_CATALOG["law firm"]
    elif "tech" in niche_lower or "software" in niche_lower or "it" in niche_lower or "cyber" in niche_lower or "digital" in niche_lower:
        return THEMES_CATALOG["technology"]
    elif "fashion" in niche_lower or "clothing" in niche_lower or "boutique" in niche_lower or "jewelry" in niche_lower:
        return THEMES_CATALOG["fashion"]
    
    return THEMES_CATALOG["default"]
