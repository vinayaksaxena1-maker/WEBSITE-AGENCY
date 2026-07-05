from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from database.database import Base
from datetime import datetime, timezone

class LeadScore(Base):
    __tablename__ = "lead_scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("search_leads.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    lead_score = Column(Integer, nullable=False)
    priority_level = Column(String(50), nullable=False)
    business_value_index = Column(Float, nullable=False)
    ai_processing_decision = Column(String(50), nullable=False)
    improvement_opportunities = Column(Text, nullable=True)
    schema_version = Column(String(10), nullable=False, default="1.0.0")
    rules_version = Column(String(10), nullable=False, default="1.0.0")
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<LeadScore(id={self.id}, lead_id={self.lead_id}, lead_score={self.lead_score}, priority_level='{self.priority_level}')>"
