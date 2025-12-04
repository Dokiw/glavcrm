import json
from typing import Optional, List

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime as dt, timezone as tz
from app.handlers.subleadevent.interfaces import AsyncSubLeadEventRepo
from app.handlers.subleadevent.schemas import CreateSubLeadEvent, OutSubLeadEvent, UpdateSubLeadEvent
from app.models import SubLeadEvent


class SubLeadEventRepo(AsyncSubLeadEventRepo):

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    async def _to_dto(m: "SubLeadEvent"):
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return OutSubLeadEvent(
            id=m.id,
            sub_lead_id=m.sub_lead_id,
            event_type=m.event_type,
            payload=m.payload,
            created_at=m.created_at
        )

    async def create_sub_lead_event(self, data: CreateSubLeadEvent) -> OutSubLeadEvent:
        m = SubLeadEvent()
        m.created_at = dt.now(tz.utc)
        m.sub_lead_id = data.sub_lead_id
        m.event_type = data.event_type
        m.payload = data.payload

        self.db.add(m)
        await self.db.flush()

        return await self._to_dto(m)

    async def update_sub_lead_event(self, data: UpdateSubLeadEvent) -> Optional[OutSubLeadEvent]:

        stmt = (
            update(SubLeadEvent)
            .where(SubLeadEvent.id == data.id)
            .values(
                sub_lead_id=data.sub_lead_id,
                event_type=data.event_type,
                payload=data.payload,
            )
            .returning(SubLeadEvent)
        )

        result = await self.db.execute(stmt)
        result = result.scalar()
        return await self._to_dto(result) if result else None

    async def get_sub_lead_event_by_id(self, id: int) -> Optional[OutSubLeadEvent]:
        res = await self.db.get(SubLeadEvent, id)
        return await self._to_dto(res) if res else None

    async def get_sub_lead_event_by_sub_lead_id(self, sub_lead_id: int) -> List[OutSubLeadEvent]:

        stmt = (
            select(SubLeadEvent)
            .where(SubLeadEvent.sub_lead_id == sub_lead_id)
            .order_by()
        )

        results = await self.db.execute(stmt)
        results = results.scalars()
        return [await self._to_dto(res) for res in results]
