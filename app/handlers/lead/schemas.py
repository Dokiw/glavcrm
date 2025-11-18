import uuid
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ---- Request / Input ----


class SubLeadCreate(BaseModel):
    master_lead_id: int = Field(..., alias="masterLeadId")
    department_id: uuid.UUID = Field(..., alias="departmentId")
    pipeline_id: int = Field(..., alias="pipelineId")
    stage_id: Optional[int] = Field(None, alias="stageId")
    status: Optional[str] = Field(None, alias="status")
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metaData")

    class Config:
        validate_by_name = True
        from_attributes = True


class SubLeadUpdate(BaseModel):
    id: int = Field(..., alias="id")
    master_lead_id: Optional[int] = Field(None, alias="masterLeadId")
    department_id: Optional[uuid.UUID] = Field(None, alias="departmentId")
    pipeline_id: Optional[int] = Field(None, alias="pipelineId")
    stage_id: Optional[int] = Field(None, alias="stageId")
    status: Optional[str] = Field(None, alias="status")
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metaData")
    version: Optional[int] = Field(None, alias="version")

    class Config:
        validate_by_name = True
        from_attributes = True


class SubLeadOut(BaseModel):
    id: int = Field(..., alias="id")
    master_lead_id: int = Field(..., alias="masterLeadId")
    department_id: uuid.UUID = Field(..., alias="departmentId")
    pipeline_id: int = Field(..., alias="pipelineId")
    stage_id: Optional[int] = Field(None, alias="stageId")
    status: str = Field(..., alias="status")
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metaData")
    version: int = Field(..., alias="version")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        validate_by_name = True
        from_attributes = True


class MasterLeadCreate(BaseModel):
    title: Optional[str] = Field(None, alias="title")
    payload: Optional[Dict[str, Any]] = Field(None, alias="payload")
    status: Optional[str] = Field(None, alias="status")
    completion_rule: Optional[str] = Field(None, alias="completionRule")
    created_by: Optional[uuid.UUID] = Field(None, alias="createdBy")
    contact_id: Optional[int] = Field(None, alias="contactId")
    # allow creating sub-leads together with master
    sub_leads: Optional[List[SubLeadCreate]] = Field(None, alias="subLeads")

    class Config:
        validate_by_name = True
        from_attributes = True


class MasterLeadUpdate(BaseModel):
    id: int = Field(..., alias="id")
    title: Optional[str] = Field(None, alias="title")
    payload: Optional[Dict[str, Any]] = Field(None, alias="payload")
    status: Optional[str] = Field(None, alias="status")
    completion_rule: Optional[str] = Field(None, alias="completionRule")
    closed_at: Optional[datetime] = Field(None, alias="closedAt")
    result: Optional[Dict[str, Any]] = Field(None, alias="result")
    version: Optional[int] = Field(None, alias="version")
    contact_id: Optional[int] = Field(None, alias="contactId")
    sub_leads: Optional[List[SubLeadUpdate]] = Field(None, alias="subLeads")

    class Config:
        validate_by_name = True
        from_attributes = True


class MasterLeadOut(BaseModel):
    id: int = Field(..., alias="id")
    title: Optional[str] = Field(None, alias="title")
    payload: Optional[Dict[str, Any]] = Field(None, alias="payload")
    status: str = Field(..., alias="status")
    completion_rule: str = Field(..., alias="completionRule")
    created_by: Optional[uuid.UUID] = Field(None, alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    closed_at: Optional[datetime] = Field(None, alias="closedAt")
    result: Optional[Dict[str, Any]] = Field(None, alias="result")
    version: int = Field(..., alias="version")
    contact_id: Optional[int] = Field(None, alias="contactId")
    sub_leads: Optional[List[SubLeadOut]] = Field(None, alias="subLeads")

    class Config:
        validate_by_name = True
        from_attributes = True