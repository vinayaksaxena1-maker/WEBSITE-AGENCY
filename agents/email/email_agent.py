from typing import Dict, Any
from core.logger import logger
from agents.email.email_contracts import FinalEmailPackage

# Import all modules
from agents.email.input_manager import InputManager
from agents.email.context_builder import ContextBuilder
from agents.email.personalization_manager import PersonalizationManager
from agents.email.prompt_builder import PromptBuilder
from agents.email.ai_generation_manager import AIGenerationManager
from agents.email.email_validator import EmailValidator
from agents.email.output_formatter import OutputFormatter
from agents.email.metadata_generator import MetadataGenerator

class EmailAgent:
    def __init__(self):
        self.name = "AI Personalized Email Engine"

    async def generate_outreach_email(self, raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates sequential execution of the 8 email modules using strong Pydantic contracts.
        Enforces strict fail-fast error propagation.
        """
        logger.info("EmailAgent: Commencing contract-validated email generation workflow.")
        try:
            # Stage 1: Load and validate inputs using UnifiedInputPackage schema
            input_package = InputManager.load_inputs(raw_inputs)
            
            # Stage 2: Context Builder aggregates to UnifiedBusinessContext
            context = ContextBuilder.build_context(input_package)
            
            # Stage 3: Personalization Manager creates PersonalizationContext
            personalization = PersonalizationManager.prepare_personalization(context)
            
            # Stage 4: Prompt Builder creates AIPromptPackage
            prompt = PromptBuilder.build_prompt(personalization)
            
            # Stage 5: AI Generation crafts GeneratedEmailDraft
            generated_email = await AIGenerationManager.generate_email(prompt)
            
            # Stage 6: Validation checks yield ValidatedEmailDraft & report
            validated_email, validation_report = EmailValidator.validate_draft(generated_email)
            
            # Stage 7: Formatting wraps draft into FormattedEmailPackage HTML DTO
            formatted_package = OutputFormatter.format_output(validated_email)
            
            # Stage 8: Metadata Generator creates FinalEmailPackage
            metadata, final_package = MetadataGenerator.generate_metadata(formatted_package, validation_report)
            
            assert isinstance(final_package, FinalEmailPackage)
            logger.info("EmailAgent: Sequential execution and contract checks completed successfully.")
            return {
                "success": True,
                "final_package": final_package.model_dump()
            }
            
        except Exception as e:
            logger.error(f"EmailAgent: Execution aborted at runtime: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
