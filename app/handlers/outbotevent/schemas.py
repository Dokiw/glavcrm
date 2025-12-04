from typing import Optional, Any, Dict, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ---- Request / Input ----
class CreateOutBox(BaseModel):
    aggregate_type: str = Field(...)
    aggregate_id: int = Field(...)
    event_type: str = Field(...)
    payload: Dict[str, Any] = Field(default_factory=dict)
    processed: bool = Field(...)
    status: str = Field(...)


class CreateOutBoxList(BaseModel):
    events: List[CreateOutBox]


# ---- Request / Output ----

class OutBoxOutPut(BaseModel):
    id: int = Field(...)
    aggregate_type: str = Field(...)
    aggregate_id: int = Field(...)
    event_type: str = Field(...)
    payload: Dict[str, Any] = Field(...)
    idempotency_key: Optional[str] = Field(None)
    processed: bool = Field(...)
    processed_at: Optional[datetime] = Field(None)
    created_at: datetime = Field(...)
    status: str = Field(...)
    error: Optional[str] = Field(None)

