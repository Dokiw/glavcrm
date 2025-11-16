import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base


class SubLead(Base):
    __tablename__ = "sub_lead"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    master_lead_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("master_lead.id", ondelete="CASCADE"), nullable=False
    )

    department_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)

    pipeline_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("department_pipeline.id", ondelete="CASCADE"), nullable=False
    )

    stage_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("pipeline_stage.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default=text("'pending'"))
    meta_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # relationships
    master: Mapped["MasterLead"] = relationship("MasterLead", back_populates="sub_leads")
    pipeline: Mapped["DepartmentPipeline"] = relationship("DepartmentPipeline", back_populates="sub_leads")
    stage: Mapped[Optional["PipelineStage"]] = relationship("PipelineStage")
    assignment: Mapped[Optional["Assignment"]] = relationship(
        "Assignment", back_populates="sub_lead", uselist=False, cascade="all, delete-orphan", passive_deletes=True
    )
    events: Mapped[List["SubLeadEvent"]] = relationship(
        "SubLeadEvent", back_populates="sub_lead", cascade="all, delete-orphan", passive_deletes=True
    )
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="sub_lead", cascade="all, delete-orphan", passive_deletes=True)

