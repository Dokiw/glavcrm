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


class DepartmentPipeline(Base):
    __tablename__ = "department_pipeline"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    department_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationships
    stages: Mapped[List["PipelineStage"]] = relationship(
        "PipelineStage", back_populates="pipeline", cascade="all, delete-orphan", passive_deletes=True
    )
    sub_leads: Mapped[List["SubLead"]] = relationship(
        "SubLead", back_populates="pipeline", cascade="all, delete-orphan", passive_deletes=True
    )


class PipelineStage(Base):
    __tablename__ = "pipeline_stage"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pipeline_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("department_pipeline.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    meta_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # relationship
    pipeline: Mapped["DepartmentPipeline"] = relationship("DepartmentPipeline", back_populates="stages")



