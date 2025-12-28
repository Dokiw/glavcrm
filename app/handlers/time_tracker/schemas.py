import datetime
import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, model_validator
import datetime as dt
from datetime import datetime

from enum import Enum


class CreateTimeTracker(BaseModel):
    task_id: int = Field(...)
    payment: bool = Field(...)
    status: Optional[str] = Field(None)
    meta_data: Optional[Dict[str, Any]] = Field(None)


class UpdateTimeTracker(BaseModel):
    id: int = Field(...)
    operating: Optional[int] = Field(None)
    payment: Optional[bool] = Field(None)
    status: Optional[str] = Field(None)
    meta_data: Optional[Dict[str, Any]] = Field(None)


class OutTimeTracker(BaseModel):
    id: int = Field(...)
    task_id: int = Field(...)
    operating: int = Field(...)
    payment: bool = Field(...)
    status: Optional[str] = Field(None)
    meta_data: Optional[Dict[str, Any]] = Field(None)
    completed_at: Optional[datetime] = Field(None)
    created_at: datetime = Field(...)
