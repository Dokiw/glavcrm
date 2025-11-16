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


class MasterLead(Base):
    __tablename__ = "master_lead"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default=text("'open'"))
    completion_rule: Mapped[str] = mapped_column(String(32), nullable=False, server_default=text("'ALL_DONE'"))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))

    # relationships
    sub_leads: Mapped[List["SubLead"]] = relationship(
        "SubLead", back_populates="master", cascade="all, delete-orphan", passive_deletes=True
    )

    contact_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("contact.id", ondelete="SET NULL"), nullable=True
    )

    contact: Mapped[Optional["Contact"]] = relationship("Contact", back_populates="master")
