from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.database import Base

class SearchLead(Base):
    __tablename__ = "search_leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(255), unique=True, nullable=False, index=True)
    source = Column(String(100), nullable=False)
    niche = Column(String(100), nullable=False)
    status = Column(String(50), default="DISCOVERED", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<SearchLead(id={self.id}, domain='{self.domain}', niche='{self.niche}', status='{self.status}')>"
