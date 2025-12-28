from typing import Optional, List

from fastapi import APIRouter

from app.handlers.subleadevent.dependencies import SubLeadEventServiceDep
from app.handlers.subleadevent.schemas import OutSubLeadEvent, CreateSubLeadEvent, UpdateSubLeadEvent

router_sub_lead_event = APIRouter(prefix="/SubLeadEvent", tags=["SubLeadEvent"])


@router_sub_lead_event.get("/{sub_lead_event_id}", response_model=Optional[OutSubLeadEvent])
async def get_sub_lead_event_by_id(
        service_sub_lead_event: SubLeadEventServiceDep,
        sub_lead_event_id: int,
):
    return await service_sub_lead_event.get_sub_lead_event_by_id(sub_lead_event_id)


@router_sub_lead_event.get("", response_model=List[OutSubLeadEvent])
async def get_sub_lead_event_by_sub_lead_id(
        service_sub_lead_event: SubLeadEventServiceDep,
        sub_lead_id: int,
):
    return await service_sub_lead_event.get_sub_lead_event_by_sub_lead_id(sub_lead_id)


@router_sub_lead_event.post("/create", response_model=OutSubLeadEvent)
async def create_sub_lead_event(
        service_sub_lead_event: SubLeadEventServiceDep,
        data: CreateSubLeadEvent
):
    return await service_sub_lead_event.create_sub_lead_event(data)


@router_sub_lead_event.patch("/update", response_model=Optional[OutSubLeadEvent])
async def update_sub_lead_event(
        service_sub_lead_event: SubLeadEventServiceDep,
        data: UpdateSubLeadEvent
):
    return await service_sub_lead_event.update_sub_lead_event(data)




