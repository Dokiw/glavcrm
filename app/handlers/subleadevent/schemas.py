from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


# ------ request \ input
class CreateSubLeadEvent(BaseModel):
    sub_lead_id: int = Field(...)
    event_type: str = Field(...)
    payload: Optional[Dict[str, Any]] = Field(None)


class UpdateSubLeadEvent(BaseModel):
    id: int = Field(...)
    sub_lead_id: Optional[int] = Field(None)
    event_type: Optional[str] = Field(None)
    payload: Optional[Dict[str, Any]] = Field(None)


# ------ request \ output
class OutSubLeadEvent(BaseModel):
    id: int = Field(...)
    sub_lead_id: int = Field(...)
    event_type: str = Field(...)
    payload: Optional[Dict[str, Any]] = Field(None)
    created_at: datetime = Field(...)
