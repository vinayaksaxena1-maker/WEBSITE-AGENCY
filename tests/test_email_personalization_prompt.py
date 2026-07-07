import pytest
from agents.email.email_contracts import UnifiedBusinessContext
from agents.email.personalization_manager import PersonalizationManager
from agents.email.prompt_builder import PromptBuilder

def test_personalization_score_branches():
    # Branch 1: mobile_score < 70
    ctx_1 = UnifiedBusinessContext(
        target_domain="fitsport.com",
        target_niche="Gym",
        target_email="jane@fitsport.com",
        audit_score=85,
        mobile_score=65,
        speed_score=80,
        prototype_url="http://proto.com",
        contact_name="Jane Doe"
    )
    p_1 = PersonalizationManager.prepare_personalization(ctx_1)
    assert p_1.modernization_hook == "mobile responsiveness optimization"
    assert p_1.niche_terminology == "mobile viewport adapter"
    
    # Branch 2: mobile_score >= 70, speed_score < 60
    ctx_2 = UnifiedBusinessContext(
        target_domain="fitsport.com",
        target_niche="Gym",
        target_email="jane@fitsport.com",
        audit_score=85,
        mobile_score=75,
        speed_score=55,
        prototype_url="http://proto.com",
        contact_name="Jane Doe"
    )
    p_2 = PersonalizationManager.prepare_personalization(ctx_2)
    assert p_2.modernization_hook == "page speed performance caching"
    assert p_2.niche_terminology == "optimized load distribution"
    
    # Branch 3: Both high
    ctx_3 = UnifiedBusinessContext(
        target_domain="fitsport.com",
        target_niche="Gym",
        target_email="jane@fitsport.com",
        audit_score=85,
        mobile_score=80,
        speed_score=75,
        prototype_url="http://proto.com",
        contact_name="Jane Doe"
    )
    p_3 = PersonalizationManager.prepare_personalization(ctx_3)
    assert p_3.modernization_hook == "visual design system modernization"
    assert p_3.niche_terminology == "glassmorphic presentation layers"

def test_prompt_construction_completeness():
    ctx = UnifiedBusinessContext(
        target_domain="fitsport.com",
        target_niche="Gym",
        target_email="jane@fitsport.com",
        audit_score=85,
        mobile_score=75,
        speed_score=55,
        prototype_url="http://proto.com",
        contact_name="Jane Doe"
    )
    p = PersonalizationManager.prepare_personalization(ctx)
    prompt_pkg = PromptBuilder.build_prompt(p)
    
    compiled = prompt_pkg.variables["compiled_prompt"]
    
    # Assert all mandatory sections exist in the compiled prompt layout
    required_sections = [
        "# SYSTEM INSTRUCTIONS",
        "# ENTERPRISE WRITING RULES",
        "# BUSINESS CONTEXT",
        "# RECIPIENT CONTEXT",
        "# AUDIT CONTEXT",
        "# PROTOTYPE CONTEXT",
        "# PERSONALIZATION VARIABLES",
        "# OUTPUT REQUIREMENTS",
        "# FORMATTING RULES",
        "# GENERATION CONSTRAINTS"
    ]
    
    for section in required_sections:
        assert section in compiled
