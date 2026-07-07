from typing import Dict, Any
from core.logger import logger
from agents.crm.crm_contracts import CRMExecutionPackageContract

# Import all modules
from agents.crm.input_manager import InputManager
from agents.crm.crm_context_builder import CRMContextBuilder
from agents.crm.relationship_manager import RelationshipManager
from agents.crm.lifecycle_manager import LifecycleManager
from agents.crm.output_validator import OutputValidator
from agents.crm.package_formatter import PackageFormatter
from agents.crm.metadata_generator import MetadataGenerator

class CRMAgent:
    def __init__(self):
        self.name = "CRM Engine"

    async def execute_crm(self, raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates sequential execution of the CRM Engine sub-phases (10.0 to 10.11).
        Enforces strict sequential execution and contract validation checks.
        """
        logger.info("CRMAgent: Commencing CRM Engine workflow pipeline.")
        try:
            # 1. Input Acquisition (UnifiedInputContract)
            input_contract = InputManager.load_inputs(raw_inputs)
            logger.info("CRMAgent: Stage 1 - Input Acquisition successful.")
            
            # 2. CRM Context Assembly (CRMContextContract)
            context_contract = CRMContextBuilder.build_context(input_contract)
            logger.info(f"CRMAgent: Stage 2 - CRM context assembled (ID: {context_contract.crm_id}).")
            
            # 3. Relationship Management (RelationshipContract)
            relationship_contract = RelationshipManager.create_relationship(context_contract)
            logger.info(f"CRMAgent: Stage 3 - Relationship created (ID: {relationship_contract.relationship_id}).")
            
            # 4. Lifecycle Initialization (LifecycleContract)
            lifecycle_contract = LifecycleManager.initialize_lifecycle(relationship_contract)
            logger.info("CRMAgent: Stage 4 - Lifecycle initialized successfully.")
            
            # 5. Output Validation (ValidatedCRMContract)
            validated_contract = OutputValidator.validate_package(context_contract, relationship_contract, lifecycle_contract)
            logger.info(f"CRMAgent: Stage 5 - Output validation passed (Validation ID: {validated_contract.validation_identifier}).")
            
            # 6. Package Formatting (Dict containing Formatted CRM Package)
            formatted_dict = PackageFormatter.format_package(validated_contract)
            logger.info("CRMAgent: Stage 6 - Package formatting completed.")
            
            # 7. Metadata Generation & Sealing (CRMExecutionPackageContract)
            final_package = MetadataGenerator.generate_metadata(formatted_dict)
            logger.info(f"CRMAgent: Stage 7 - Metadata generated and package sealed (Execution ID: {final_package.metadata_package.execution_identifier}).")
            
            assert isinstance(final_package, CRMExecutionPackageContract)
            return {
                "success": True,
                "final_package": final_package.model_dump()
            }
            
        except Exception as e:
            logger.error(f"CRMAgent: Execution pipeline aborted at runtime: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
