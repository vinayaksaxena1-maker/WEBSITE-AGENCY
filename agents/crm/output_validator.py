import uuid
from agents.crm.crm_contracts import (
    CRMContextContract,
    RelationshipContract,
    LifecycleContract,
    ValidatedCRMContract
)

class OutputValidator:
    @staticmethod
    def validate_package(
        context: CRMContextContract,
        relationship: RelationshipContract,
        lifecycle: LifecycleContract
    ) -> ValidatedCRMContract:
        """
        Validates the assembled CRM sub-components and generates the ValidatedCRMContract.
        """
        errors = []
        
        # 1. Structural Validation
        if not context.crm_id:
            errors.append("Missing context.crm_id")
        if not relationship.relationship_id:
            errors.append("Missing relationship.relationship_id")
        if relationship.crm_id != context.crm_id:
            errors.append("Relationship crm_id does not match context crm_id")
            
        # 2. Relationship validation
        if not relationship.customer_references.get("customer_email"):
            errors.append("Missing customer email in relationship references")
            
        # 3. Lifecycle validation
        if lifecycle.relationship_state.get("current_relationship_status") != "ACTIVE":
            errors.append("Relationship status is not ACTIVE in lifecycle state")
            
        if errors:
            raise ValueError(f"CRM Output validation failed: {'; '.join(errors)}")
            
        validation_identifier = f"VAL-CRM-{uuid.uuid4().hex[:12].upper()}"
        
        # Set validation details in the approved records
        approved_crm_record = context.model_dump()
        approved_relationship = relationship.model_dump()
        approved_lifecycle = lifecycle.model_dump()
        
        approved_relationship["relationship_metadata"]["validation_reference"] = validation_identifier
        approved_relationship["execution_references"]["validation_identifier"] = validation_identifier
        approved_lifecycle["lifecycle_metadata"]["validation_reference"] = validation_identifier
        
        return ValidatedCRMContract(
            approved_crm_record=approved_crm_record,
            approved_relationship_information=approved_relationship,
            approved_lifecycle_information=approved_lifecycle,
            validation_status="PASSED",
            validation_identifier=validation_identifier
        )
