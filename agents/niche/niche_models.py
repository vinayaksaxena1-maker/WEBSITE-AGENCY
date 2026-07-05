from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime, timezone

class BusinessProfile(Base):
    __tablename__ = "business_profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("search_leads.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    industry = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    recommended_theme = Column(String(100), nullable=False)
    schema_version = Column(String(10), nullable=False, default="1.0.0")
    classifier_version = Column(String(10), nullable=False, default="1.0.0")
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<BusinessProfile(id={self.id}, lead_id={self.lead_id}, industry='{self.industry}', confidence={self.confidence})>"
