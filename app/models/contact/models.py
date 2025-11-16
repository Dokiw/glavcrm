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


# Дописать

class Contact(Base):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    number: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    name: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)

    family: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)

    company: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)

    description: Mapped[str] = mapped_column(String(), unique=False, nullable=True)

    master: Mapped[List["MasterLead"]] = relationship(
        "MasterLead",
        back_populates="contact",
        cascade="all, delete-orphan"
    )