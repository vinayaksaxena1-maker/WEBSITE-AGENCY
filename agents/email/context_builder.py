from agents.email.email_contracts import UnifiedInputPackage, UnifiedBusinessContext

class ContextBuilder:
    @staticmethod
    def build_context(input_package: UnifiedInputPackage) -> UnifiedBusinessContext:
        """
        Aggregates inputs into a normalized UnifiedBusinessContext contract.
        """
        lead = input_package.lead_profile
        audit = input_package.audit_report
        proto = input_package.prototype_report
        contact = input_package.contact_info
        
        # Domain Normalization & Protocol Cleanup
        domain = lead.domain.lower().strip()
        prefixes = ["https://", "http://", "www."]
        for prefix in prefixes:
            if domain.startswith(prefix):
                domain = domain[len(prefix):]
                
        # Email Normalization
        email = contact.email.lower().strip()
        
        # Build Context
        return UnifiedBusinessContext(
            target_domain=domain,
            target_niche=lead.niche.strip(),
            target_email=email,
            audit_score=audit.audit_score,
            mobile_score=audit.mobile_score,
            speed_score=audit.speed_score,
            prototype_url=proto.prototype_url.strip(),
            contact_name=contact.name.strip()
        )
