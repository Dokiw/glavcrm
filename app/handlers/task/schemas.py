import datetime
import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, model_validator
import datetime as dt
from datetime import datetime

from enum import Enum


class CreateTask(BaseModel):
    sub_lead_id: Optional[int] = Field(None)
    assigned_to: Optional[uuid.UUID] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    status: str = Field()
    due_date: Optional[datetime] = Field(None)
    meta_data: Optional[Dict[str, Any]] = Field(None)

    model_config = {
        "validate_by_name": True,
        "from_attributes": True
    }


class UpdateTask(BaseModel):
    id: int = Field(...)
    sub_lead_id: Optional[int] = Field(None)
    assigned_to: Optional[uuid.UUID] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    due_date: Optional[datetime] = Field(None)
    meta_data: Optional[Dict[str, Any]] = Field(None)

    model_config = {
        "validate_by_name": True,
        "from_attributes": True
    }


class OutTask(BaseModel):
    id: int = Field(...)
    sub_lead_id: Optional[int] = Field(None)
    assigned_to: Optional[uuid.UUID] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    due_date: Optional[datetime] = Field(None)
    meta_data: Optional[Dict[str, Any]] = Field(None)

    model_config = {
        "validate_by_name": True,
        "from_attributes": True
    }
