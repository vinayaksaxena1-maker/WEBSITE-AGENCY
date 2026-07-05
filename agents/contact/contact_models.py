from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("search_leads.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    primary_email = Column(String(255), nullable=True)
    secondary_email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    whatsapp = Column(String(50), nullable=True)
    facebook = Column(String(255), nullable=True)
    instagram = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    youtube = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Contact(id={self.id}, lead_id={self.lead_id}, status='{self.status}')>"
