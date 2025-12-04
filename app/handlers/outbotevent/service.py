from typing import List, Optional

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.outbotevent.interfaces import AsyncOutBoxService, AsyncOutBoxRepository
from app.handlers.outbotevent.schemas import CreateOutBoxList, OutBoxOutPut, CreateOutBox


class OutBoxService(AsyncOutBoxService):

    def __init__(self, uow: IUnitOfWork[AsyncOutBoxRepository]):
        self.uow = uow

    async def create_out_box(self, event: CreateOutBox) -> OutBoxOutPut:
        return await self.uow.repo.create_out_box(event)

    async def create_out_box_many(self, events: CreateOutBoxList) -> List[Optional[OutBoxOutPut]]:
        return await self.uow.repo.create_out_box_many(events)
