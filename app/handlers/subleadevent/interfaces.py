from typing import Protocol, List, Optional

from app.handlers.subleadevent.schemas import CreateSubLeadEvent, OutSubLeadEvent, UpdateSubLeadEvent


class AsyncSubLeadEventRepo(Protocol):

    async def create_sub_lead_event(self, data: CreateSubLeadEvent) -> OutSubLeadEvent:
        ...

    async def update_sub_lead_event(self, data: UpdateSubLeadEvent) -> Optional[OutSubLeadEvent]:
        ...

    async def get_sub_lead_event_by_id(self, id: int) -> Optional[OutSubLeadEvent]:
        ...

    async def get_sub_lead_event_by_sub_lead_id(self, sub_lead_id: int) -> List[OutSubLeadEvent]:
        ...


class AsyncSubLeadEventService(Protocol):
    async def create_sub_lead_event(self, data: CreateSubLeadEvent) -> OutSubLeadEvent:
        ...

    async def update_sub_lead_event(self, data: UpdateSubLeadEvent) -> Optional[OutSubLeadEvent]:
        ...

    async def get_sub_lead_event_by_id(self, id: int) -> Optional[OutSubLeadEvent]:
        ...

    async def get_sub_lead_event_by_sub_lead_id(self, sub_lead_id: int) -> List[OutSubLeadEvent]:
        ...
