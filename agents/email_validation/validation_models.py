from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from database.database import Base

class ValidatedEmail(Base):
    __tablename__ = "validated_emails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("search_leads.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)
    quality_score = Column(Integer, nullable=False)
    classification = Column(String(50), nullable=False)
    mx_status = Column(String(50), nullable=False)
    domain_status = Column(String(50), nullable=False)
    disposable = Column(Boolean, nullable=False, default=False)
    role_based = Column(Boolean, nullable=False, default=False)
    confidence = Column(Float, nullable=False)
    recommended_action = Column(String(50), nullable=False)
    validated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<ValidatedEmail(id={self.id}, lead_id={self.lead_id}, email='{self.email}', score={self.quality_score})>"
