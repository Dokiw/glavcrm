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


class SubLeadEvent(Base):
    __tablename__ = "sub_lead_event"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sub_lead_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sub_lead.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationship
    sub_lead: Mapped["SubLead"] = relationship("SubLead", back_populates="events")
