import uuid
from datetime import datetime, timezone
from typing import Tuple
from agents.email.email_contracts import (
    FormattedEmailPackage,
    FinalEmailPackage,
    ValidationReportContract,
    ProcessingMetadataContract,
    PublicationMetadataContract,
    FinalEmailPackageMetadata
)

class MetadataGenerator:
    @staticmethod
    def generate_metadata(
        formatted_package: FormattedEmailPackage,
        validation_report: ValidationReportContract
    ) -> Tuple[FinalEmailPackageMetadata, FinalEmailPackage]:
        """
        Generates tracking execution metadata and seals the final email package using Pydantic contracts.
        """
        exec_id = str(uuid.uuid4())
        current_time = datetime.now(timezone.utc).isoformat()
        is_pass = validation_report.status == "PASS"
        
        proc_meta = ProcessingMetadataContract(
            processing_timestamp=current_time,
            processing_status="PASS" if is_pass else "FAIL",
            execution_duration_sec=0.01,
            completion_status="SUCCESS" if is_pass else "FAILURE"
        )
        
        pub_meta = PublicationMetadataContract(
            publication_status="PUBLISHED" if is_pass else "REJECTED",
            publication_timestamp=current_time,
            output_package_identifier=str(uuid.uuid4())
        )
        
        metadata = FinalEmailPackageMetadata(
            execution_id=exec_id,
            validation_status="PASS" if is_pass else "FAIL",
            validation_report=validation_report,
            processing_metadata=proc_meta,
            publication_metadata=pub_meta
        )
        
        final_package = FinalEmailPackage(
            email_payload=formatted_package,
            metadata=metadata
        )
        
        return metadata, final_package
