from typing import Dict, Any
from core.logger import logger
from agents.followup.followup_contracts import FollowUpExecutionPackageContract

# Import all modules
from agents.followup.input_manager import InputManager
from agents.followup.workflow_builder import WorkflowBuilder
from agents.followup.sequence_manager import SequenceManager
from agents.followup.state_manager import StateManager
from agents.followup.output_validator import OutputValidator
from agents.followup.package_formatter import PackageFormatter
from agents.followup.metadata_generator import MetadataGenerator

class FollowUpAgent:
    def __init__(self):
        self.name = "Follow-Up Engine"

    async def execute_followup(self, raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates sequential execution of the Follow-Up Engine sub-phases (9.1 to 9.11).
        Enforces strict sequential execution and contract validation checks.
        """
        logger.info("FollowUpAgent: Commencing Follow-Up Engine workflow pipeline.")
        try:
            # 1. Input Acquisition (UnifiedInputContract)
            input_contract = InputManager.load_inputs(raw_inputs)
            logger.info("FollowUpAgent: Stage 1 - Input Acquisition successful.")
            
            # 2. Workflow Context Assembly (WorkflowContextContract)
            context_contract = WorkflowBuilder.build_context(input_contract)
            logger.info(f"FollowUpAgent: Stage 2 - Workflow context assembled (ID: {context_contract.workflow_id}).")
            
            # 3. Sequence Preparation (FollowUpSequenceContract)
            sequence_contract = SequenceManager.build_sequence(context_contract)
            logger.info(f"FollowUpAgent: Stage 3 - Sequence prepared (ID: {sequence_contract.sequence_id}).")
            
            # 4. State Initialization (FollowUpStateContract)
            state_contract = StateManager.initialize_state(sequence_contract)
            logger.info("FollowUpAgent: Stage 4 - State initialization successful.")
            
            # 5. Output Validation (ValidatedFollowUpContract)
            validated_contract = OutputValidator.validate_package(context_contract, sequence_contract, state_contract)
            logger.info(f"FollowUpAgent: Stage 5 - Output validation passed (Validation ID: {validated_contract.validation_id}).")
            
            # 6. Package Formatting (Dict containing Formatted Follow-Up Package)
            formatted_dict = PackageFormatter.format_package(validated_contract)
            logger.info("FollowUpAgent: Stage 6 - Package formatting completed.")
            
            # 7. Metadata Generation & Sealing (FollowUpExecutionPackageContract)
            final_package = MetadataGenerator.generate_metadata(formatted_dict)
            logger.info(f"FollowUpAgent: Stage 7 - Metadata generated and package sealed (Execution ID: {final_package.metadata_package.execution_id}).")
            
            assert isinstance(final_package, FollowUpExecutionPackageContract)
            return {
                "success": True,
                "final_package": final_package.model_dump()
            }
            
        except Exception as e:
            logger.error(f"FollowUpAgent: Execution pipeline aborted at runtime: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
