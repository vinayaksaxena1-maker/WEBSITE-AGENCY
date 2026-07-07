from typing import Dict, Any
from agents.crm.crm_contracts import ValidatedCRMContract

class PackageFormatter:
    @staticmethod
    def format_package(validated: ValidatedCRMContract) -> Dict[str, Any]:
        """
        Formats and normalizes validated CRM information for downstream systems.
        """
        validation_report = {
            "validation_identifier": validated.validation_identifier,
            "structural_validation": "PASS",
            "crm_validation": "PASS",
            "relationship_validation": "PASS",
            "lifecycle_validation": "PASS",
            "formatting_validation": "PASS",
            "overall_validation_result": "VALID"
        }
        
        formatted_crm_package = {
            "crm_information": validated.approved_crm_record,
            "relationship_information": validated.approved_relationship_information,
            "lifecycle_information": validated.approved_lifecycle_information,
            "validation_information": validation_report,
            "processing_information": validated.approved_lifecycle_information["processing_state"],
            "packaging_status": "COMPLETED"
        }
        
        return {
            "formatted_crm_package": formatted_crm_package,
            "validation_report": validation_report,
            "processing_status": "COMPLETED"
        }
