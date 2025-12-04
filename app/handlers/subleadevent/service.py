from typing import Optional, List

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.subleadevent.interfaces import AsyncSubLeadEventService, AsyncSubLeadEventRepo
from app.handlers.subleadevent.schemas import CreateSubLeadEvent, OutSubLeadEvent, UpdateSubLeadEvent
from app.method.decorator import transactional


class SubLeadEventService(AsyncSubLeadEventService):

    def __init__(self, uow: IUnitOfWork[AsyncSubLeadEventRepo]):
        self.uow = uow

    @transactional()
    async def create_sub_lead_event(self, data: CreateSubLeadEvent) -> OutSubLeadEvent:
        return await self.uow.repo.create_sub_lead_event(data)

    @transactional()
    async def update_sub_lead_event(self, data: UpdateSubLeadEvent) -> Optional[OutSubLeadEvent]:
        return await self.uow.repo.update_sub_lead_event(data)

    @transactional()
    async def get_sub_lead_event_by_id(self, id: int) -> Optional[OutSubLeadEvent]:
        return await self.uow.repo.get_sub_lead_event_by_id(id)

    @transactional()
    async def get_sub_lead_event_by_sub_lead_id(self, sub_lead_id: int) -> List[OutSubLeadEvent]:
        return await self.uow.repo.get_sub_lead_event_by_sub_lead_id(sub_lead_id)
