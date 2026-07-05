from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database.database import Base

class Audit(Base):
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("search_leads.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    schema_version = Column(String(10), nullable=False)
    audit_rule_version = Column(String(10), nullable=False)
    audit_score = Column(Integer, nullable=False)
    seo_score = Column(Integer, nullable=False)
    mobile_score = Column(Integer, nullable=False)
    speed_score = Column(Integer, nullable=False)
    trust_score = Column(Integer, nullable=False)
    design_score = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Audit(id={self.id}, lead_id={self.lead_id}, audit_score={self.audit_score})>"
