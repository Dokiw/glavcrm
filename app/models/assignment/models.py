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


class Assignment(Base):
    __tablename__ = "assignment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sub_lead_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sub_lead.id", ondelete="CASCADE"), nullable=False, unique=True)

    wait_mode: Mapped[str] = mapped_column(String(16), nullable=False, server_default=text("'mandatory'"))
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    meta_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # relationship
    sub_lead: Mapped["SubLead"] = relationship("SubLead", back_populates="assignment")
