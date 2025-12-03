from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.task.interfaces import AsyncOutBoxRepository
from app.models import Outbox


class OutBoxRepository(AsyncOutBoxRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, event: dict):

        stmt = insert(Outbox).values(event)
        await self.db.execute(stmt)

    async def add_many(self, events: list[dict]):
        if events:
            stmt = insert(Outbox).values(events)
            await self.db.execute(stmt)

