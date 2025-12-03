from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.task.interfaces import AsyncOutBoxService, AsyncOutBoxRepository


class OutBoxService(AsyncOutBoxService):

    def __init__(self, uow: IUnitOfWork[AsyncOutBoxRepository]):
        self.uow = uow

    async def create_out_box(self, event: dict):
        return await self.uow.repo.create_out_box(event)

    async def create_out_box_many(self, events: list[dict]):
        return await self.uow.repo.create_out_box_many(events)
