import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
import datetime as dt


# ---------------settings ----------------
class transfer_lead_pipeline_stage(BaseModel):
    enable: bool = Field(...)
    to_department: str = Field(...)
    create_sub_lead: str = Field(...)

    class Config:
        validate_by_name = True
        from_attributes = True


class create_task_pipeline(BaseModel):
    enable: bool = Field(...)
    from_whom: str = Field(...)

    class Config:
        validate_by_name = True
        from_attributes = True


class settings_pipeline_stage(BaseModel):
    transfer: transfer_lead_pipeline_stage
    create_task: create_task_pipeline

    class Config:
        validate_by_name = True
        from_attributes = True


# -------------------input------------------
class create_department(BaseModel):
    name: str = Field(..., alias="name")

    class Config:
        validate_by_name = True
        from_attributes = True


class create_pipeline_stage(BaseModel):
    pipeline_id: int = Field(..., alias="pipelineId")
    name: str = Field(..., alias="name")
    position: int = Field(..., alias="position")
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metadata")

    class Config:
        validate_by_name = True
        from_attributes = True


class update_department(BaseModel):
    id: int = Field(..., alias="id")
    name: Optional[str] = Field(None, alias="name")
    is_active: Optional[bool] = Field(None, alias="isActive")

    class Config:
        validate_by_name = True
        from_attributes = True


class update_pipeline_stage(BaseModel):
    id: int = Field(..., alias="id")
    pipeline_id: Optional[int] = Field(None, alias="pipelineId")
    name: Optional[str] = Field(None, alias="name")
    position: Optional[int] = Field(None, alias="position")
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metadata")

    class Config:
        validate_by_name = True
        from_attributes = True


# -------------- output -------------------

class output_department(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    department_id: str = Field(..., alias="departmentId")
    is_active: bool = Field(..., alias="isActive")

    created_at: dt.datetime = Field(..., alias="CreatedAt")

    class Config:
        validate_by_name = True
        from_attributes = True


class output_pipeline_stage(BaseModel):
    id: int = Field(..., alias="id")
    pipeline_id: int = Field(..., alias="pipelineId")
    name: str = Field(..., alias="name")
    position: int = Field(..., alias="position")
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metadata")

    class Config:
        validate_by_name = True
        from_attributes = True
