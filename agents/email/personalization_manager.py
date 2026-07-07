from agents.email.email_contracts import UnifiedBusinessContext, PersonalizationContext

class PersonalizationManager:
    @staticmethod
    def prepare_personalization(context: UnifiedBusinessContext) -> PersonalizationContext:
        """
        Determines personalization variables, hooks, and terminologies from Business Context.
        """
        niche = context.target_niche
        mobile_score = context.mobile_score
        speed_score = context.speed_score
        
        if mobile_score < 70:
            hook = "mobile responsiveness optimization"
            terminology = "mobile viewport adapter"
        elif speed_score < 60:
            hook = "page speed performance caching"
            terminology = "optimized load distribution"
        else:
            hook = "visual design system modernization"
            terminology = "glassmorphic presentation layers"
            
        domain_parts = context.target_domain.split('.')
        company_name = domain_parts[0].capitalize() if domain_parts else "Business Partner"
        
        return PersonalizationContext(
            target_email=context.target_email,
            contact_name=context.contact_name,
            company_name=company_name,
            target_niche=niche,
            modernization_hook=hook,
            niche_terminology=terminology,
            prototype_url=context.prototype_url,
            audit_score=context.audit_score
        )
