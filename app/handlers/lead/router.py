from typing import Optional

from fastapi import APIRouter, HTTPException

from app.handlers.lead.dependencies import MasterLeadServiceDep, SubLeadServiceDep
from app.handlers.lead.schemas import MasterLeadOut, MasterLeadCreate, MasterLeadUpdate, SubLeadOut, SubLeadUpdate, \
    SubLeadCreate, ListSubLeadOut

router_master_lead = APIRouter(prefix="/MasterLead", tags=["MasterLead"])


@router_master_lead.get("/")
async def hub():
    return HTTPException(200, 'Status - True')


@router_master_lead.get("/{master_lead_id}", response_model=Optional[MasterLeadOut])
async def get_master_lead_by_id(
        service_master_lead: MasterLeadServiceDep,
        master_lead_id: int
) -> Optional[MasterLeadOut]:
    return await service_master_lead.get_master_lead_by_id(master_lead_id)


@router_master_lead.post("/create", response_model=Optional[MasterLeadOut])
async def create_master_lead(
        service_master_lead: MasterLeadServiceDep,
        data_create: MasterLeadCreate
) -> MasterLeadOut:
    return await service_master_lead.create_master_lead(data_create)


@router_master_lead.post("/update", response_model=Optional[MasterLeadOut])
async def update_master_lead(
        service_master_lead: MasterLeadServiceDep,
        data_update: MasterLeadUpdate) -> Optional[MasterLeadOut]:
    return await service_master_lead.update_master_lead(data_update)


@router_master_lead.delete("/delete/{master_lead_id}", response_model=Optional[MasterLeadOut])
async def delete_master_lead(
        service_master_lead: MasterLeadServiceDep,
        master_lead_id: int
) -> Optional[MasterLeadOut]:
    return await service_master_lead.delete_master_lead(master_lead_id)


router_sub_lead = APIRouter(prefix="/SubLead", tags=["SubLead"])


@router_sub_lead.post("/{sub_lead_id}/next", response_model=Optional[SubLeadOut])
async def next_sub_lead_stage(
        sub_lead_service: SubLeadServiceDep,
        sub_lead_id: int
):
    return await sub_lead_service.next_sub_lead_stage(sub_lead_id)


@router_sub_lead.post("/{sub_lead_id}/move", response_model=Optional[SubLeadOut])
async def move_sub_lead_stage(
        sub_lead_service: SubLeadServiceDep,
        sub_lead_id: int,
        to_stage_id: int,
):
    return await sub_lead_service.move_sub_lead_stage(sub_lead_id, to_stage_id)


@router_sub_lead.post("/{sub_lead_id}/prev", response_model=Optional[SubLeadOut])
async def prev_sub_lead_stage(
        sub_lead_service: SubLeadServiceDep,
        sub_lead_id: int
):
    return await sub_lead_service.prev_sub_lead_stage(sub_lead_id)


@router_sub_lead.post("", response_model=Optional[ListSubLeadOut])
async def list_sub_lead_stage(
        sub_lead_service: SubLeadServiceDep,
        offset: int,
        limit: int
):
    return await sub_lead_service.list_sub_lead(offset, limit)


@router_sub_lead.post("/create", response_model=SubLeadOut)
async def create_sub_lead(
        sub_lead_service: SubLeadServiceDep,
        data_create: SubLeadCreate
) -> SubLeadOut:
    return await sub_lead_service.create_sub_lead(data_create)


@router_sub_lead.post("/update", response_model=Optional[SubLeadOut])
async def update_sub_lead(
        sub_lead_service: SubLeadServiceDep,
        data_update: SubLeadUpdate
) -> Optional[SubLeadOut]:
    return await sub_lead_service.update_sub_lead(data_update)


@router_sub_lead.get("/{sub_lead_id}", response_model=Optional[SubLeadOut])
async def get_sub_lead_by_id(
        sub_lead_service: SubLeadServiceDep,
        sub_lead_id: int
) -> Optional[SubLeadOut]:
    return await sub_lead_service.get_sub_lead_by_id(sub_lead_id)


@router_sub_lead.delete("/delete/{sub_lead_id}", response_model=Optional[SubLeadOut])
async def delete_sub_lead(
        sub_lead_service: SubLeadServiceDep,
        sub_lead_id: int
) -> Optional[SubLeadOut]:
    return await sub_lead_service.delete_sub_lead(sub_lead_id)
