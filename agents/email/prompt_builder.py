from agents.email.email_contracts import PersonalizationContext, AIPromptPackage

class PromptBuilder:
    @staticmethod
    def build_prompt(personalization: PersonalizationContext) -> AIPromptPackage:
        """
        Constructs the structured prompt instructions for AI generation.
        """
        system_instructions = "You are an enterprise sales outreach specialist for Website Agency."
        writing_rules = "Keep the email professional, brief, and convert-oriented. No generic hype."
        business_context = f"Company Name: {personalization.company_name}\nNiche: {personalization.target_niche}"
        recipient_context = f"Contact Name: {personalization.contact_name}\nEmail: {personalization.target_email}"
        audit_context = f"Website Audit Score: {personalization.audit_score}/100"
        prototype_context = f"Redesigned HTML Prototype URL: {personalization.prototype_url}"
        personalization_vars = f"Selected Modernization Highlight: {personalization.modernization_hook}\nSelected Terminology: {personalization.niche_terminology}"
        output_requirements = "Subject line: Upgrade proposal for {company_name} - Redesign Redy\nBody: Professional proposal showing value from audit and link to prototype."
        formatting_rules = "Output format: Subject line first, followed by body text."
        generation_constraints = (
            "Do not invent statistics. Do not make unverified claims. "
            "Do NOT include any placeholder brackets (e.g. '[Your Name]', '[Your Title]', '[Company]', "
            "'[Date]', '[Phone Number]') or placeholder variables under any circumstances. "
            "Sign the email strictly as 'Website Agency' and output the text directly without placeholders."
        )
        
        # Combine everything into a structured prompt
        compiled_prompt = (
            f"# SYSTEM INSTRUCTIONS\n{system_instructions}\n\n"
            f"# ENTERPRISE WRITING RULES\n{writing_rules}\n\n"
            f"# BUSINESS CONTEXT\n{business_context}\n\n"
            f"# RECIPIENT CONTEXT\n{recipient_context}\n\n"
            f"# AUDIT CONTEXT\n{audit_context}\n\n"
            f"# PROTOTYPE CONTEXT\n{prototype_context}\n\n"
            f"# PERSONALIZATION VARIABLES\n{personalization_vars}\n\n"
            f"# OUTPUT REQUIREMENTS\n{output_requirements}\n\n"
            f"# FORMATTING RULES\n{formatting_rules}\n\n"
            f"# GENERATION CONSTRAINTS\n{generation_constraints}"
        )
        
        subject_template = "Upgrade proposal for {company_name} - Redesign Redy"
        body_template = (
            "Hi {contact_name},\n\n"
            "We reviewed your website and noticed opportunities for {modernization_hook}. "
            "Our audit scored it at {audit_score}/100. We built a custom prototype with "
            "{niche_terminology} at {prototype_url} for you.\n\n"
            "Best regards,\nWebsite Agency"
        )
        
        prompt_subject = subject_template.format(company_name=personalization.company_name)
        prompt_body = body_template.format(
            contact_name=personalization.contact_name,
            modernization_hook=personalization.modernization_hook,
            audit_score=personalization.audit_score,
            niche_terminology=personalization.niche_terminology,
            prototype_url=personalization.prototype_url
        )
        
        return AIPromptPackage(
            prompt_subject=prompt_subject,
            prompt_body=prompt_body,
            target_email=personalization.target_email,
            variables={
                "compiled_prompt": compiled_prompt,
                "personalization": personalization.model_dump()
            }
        )
