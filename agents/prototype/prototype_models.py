from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from database.database import Base, db_manager

class PrototypeJob(Base):
    __tablename__ = "prototype_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("search_leads.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    website_url = Column(String(255), nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)
    theme = Column(String(100), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<PrototypeJob(id={self.id}, lead_id={self.lead_id}, url='{self.website_url}', status='{self.status}')>"


class PrototypeResult(Base):
    __tablename__ = "prototype_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    html_path = Column(String(255), nullable=True)
    css_path = Column(String(255), nullable=True)
    preview_path = Column(String(255), nullable=True)
    quality_score = Column(Integer, nullable=True)
    generation_time = Column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<PrototypeResult(id={self.id}, job_id={self.job_id}, score={self.quality_score})>"


class PrototypeReport(Base):
    __tablename__ = "prototype_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    summary = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    warnings = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<PrototypeReport(id={self.id}, job_id={self.job_id})>"


class PrototypeAsset(Base):
    __tablename__ = "prototype_assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_type = Column(String(100), nullable=False)
    asset_path = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeAsset(id={self.id}, job_id={self.job_id}, type='{self.asset_type}')>"


class PrototypeScreenshot(Base):
    __tablename__ = "prototype_screenshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    desktop_path = Column(String(255), nullable=False)
    tablet_path = Column(String(255), nullable=False)
    mobile_path = Column(String(255), nullable=False)
    fullpage_path = Column(String(255), nullable=False)
    capture_duration = Column(Float, nullable=False)
    page_height = Column(Integer, nullable=False)
    page_width = Column(Integer, nullable=False)
    browser = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="CAPTURED")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeScreenshot(id={self.id}, job_id={self.job_id}, status='{self.status}')>"


class PrototypeDOMAnalysis(Base):
    __tablename__ = "prototype_dom_analysis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    component_count = Column(Integer, nullable=False)
    section_count = Column(Integer, nullable=False)
    navigation_type = Column(String(50), nullable=False)
    layout_type = Column(String(50), nullable=False)
    cta_count = Column(Integer, nullable=False)
    form_count = Column(Integer, nullable=False)
    analysis_time = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="ANALYZED")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeDOMAnalysis(id={self.id}, job_id={self.job_id}, status='{self.status}')>"


class PrototypeVisualAnalysis(Base):
    __tablename__ = "prototype_visual_analysis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    primary_color = Column(String(7), nullable=False)
    secondary_color = Column(String(7), nullable=False)
    background_color = Column(String(7), nullable=False)
    text_color = Column(String(7), nullable=False)
    font_family = Column(String(100), nullable=False)
    visual_score = Column(Integer, nullable=False)
    analysis_time = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="ANALYZED")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeVisualAnalysis(id={self.id}, job_id={self.job_id}, status='{self.status}')>"


class PrototypeTheme(Base):
    __tablename__ = "prototype_themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    theme_name = Column(String(100), nullable=False)
    industry = Column(String(100), nullable=False)
    personality = Column(String(100), nullable=False)
    primary_color = Column(String(7), nullable=False)
    secondary_color = Column(String(7), nullable=False)
    accent_color = Column(String(7), nullable=False)
    heading_font = Column(String(100), nullable=False)
    body_font = Column(String(100), nullable=False)
    theme_score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeTheme(id={self.id}, job_id={self.job_id}, theme_name='{self.theme_name}')>"


class PrototypeComponent(Base):
    __tablename__ = "prototype_components"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    component_name = Column(String(100), nullable=False)
    variant = Column(String(50), nullable=False)
    theme = Column(String(100), nullable=False)
    priority = Column(String(20), nullable=False)
    dependencies = Column(Text, nullable=True)
    responsive_ready = Column(Boolean, nullable=False, default=True)
    accessibility_ready = Column(Boolean, nullable=False, default=True)
    status = Column(String(50), nullable=False, default="COMPILED")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeComponent(id={self.id}, job_id={self.job_id}, component_name='{self.component_name}')>"


class PrototypeTemplate(Base):
    __tablename__ = "prototype_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    layout_type = Column(String(50), nullable=False)
    columns_count = Column(Integer, nullable=False)
    section_sequence = Column(Text, nullable=False)
    tailwind_grid_class = Column(String(100), nullable=False)
    spacing_rules = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="STRUCTURED")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeTemplate(id={self.id}, job_id={self.job_id}, layout_type='{self.layout_type}')>"





class PrototypeResponsive(Base):
    __tablename__ = "prototype_responsive"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    breakpoint_profile = Column(Text, nullable=False)
    device_support = Column(Text, nullable=False)
    responsive_score = Column(Integer, nullable=False)
    validation_status = Column(String(50), nullable=False, default="PASSED")
    execution_time = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeResponsive(id={self.id}, job_id={self.job_id}, responsive_score={self.responsive_score})>"


class PrototypeBuild(Base):
    __tablename__ = "prototype_builds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    build_version = Column(String(50), nullable=False, default="1.0.0")
    component_count = Column(Integer, nullable=False)
    html_size = Column(Integer, nullable=False)
    asset_count = Column(Integer, nullable=False)
    seo_score = Column(Integer, nullable=False)
    accessibility_score = Column(Integer, nullable=False)
    validation_status = Column(String(50), nullable=False, default="PASSED")
    generation_time = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeBuild(id={self.id}, job_id={self.job_id}, build_version='{self.build_version}')>"


class PrototypePreview(Base):
    __tablename__ = "prototype_previews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    preview_version = Column(String(50), nullable=False, default="1.0.0")
    desktop_image = Column(String(300), nullable=True)
    laptop_image = Column(String(300), nullable=True)
    tablet_image = Column(String(300), nullable=True)
    mobile_image = Column(String(300), nullable=True)
    comparison_image = Column(String(300), nullable=True)
    preview_score = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypePreview(id={self.id}, job_id={self.job_id}, preview_score={self.preview_score})>"


class PrototypeQuality(Base):
    __tablename__ = "prototype_quality"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    html_score = Column(Integer, nullable=False)
    accessibility_score = Column(Integer, nullable=False)
    performance_score = Column(Integer, nullable=False)
    responsive_score = Column(Integer, nullable=False)
    seo_score = Column(Integer, nullable=False)
    ux_score = Column(Integer, nullable=False)
    visual_score = Column(Integer, nullable=False)
    component_score = Column(Integer, nullable=False)
    overall_score = Column(Integer, nullable=False)
    certification_level = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="PASSED")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeQuality(id={self.id}, job_id={self.job_id}, overall_score={self.overall_score})>"


class PrototypeExport(Base):
    __tablename__ = "prototype_exports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("prototype_jobs.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    export_version = Column(String(50), nullable=False, default="1.0.0")
    package_name = Column(String(200), nullable=False)
    package_size = Column(Integer, nullable=False)
    checksum = Column(String(100), nullable=False)
    export_status = Column(String(50), nullable=False, default="COMPLETED")
    validation_status = Column(String(50), nullable=False, default="PASSED")
    generated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<PrototypeExport(id={self.id}, job_id={self.job_id}, package_name='{self.package_name}')>"


async def init_prototype_db() -> None:
    """
    Initializes database tables for the Prototype Engine in sqlite database.
    """
    # Import validation models to register them on Base.metadata
    from agents.prototype.validation_models import PrototypeRelease
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
