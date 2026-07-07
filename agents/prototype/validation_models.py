from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.database import Base

class PrototypeRelease(Base):
    __tablename__ = "prototype_release"

    id = Column(Integer, primary_key=True, autoincrement=True)
    release_version = Column(String(50), nullable=False, default="1.0.0")
    architecture_version = Column(String(50), nullable=False, default="EDK-V7")
    certification_level = Column(String(50), nullable=False)
    overall_score = Column(Integer, nullable=False)
    production_ready = Column(Boolean, nullable=False, default=True)
    release_status = Column(String(50), nullable=False, default="PASS")
    validated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeRelease(id={self.id}, version='{self.release_version}', status='{self.release_status}')>"
