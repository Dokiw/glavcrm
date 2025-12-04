from typing import List, Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.outbotevent.interfaces import AsyncOutBoxRepository
from app.handlers.outbotevent.schemas import OutBoxOutPut, CreateOutBoxList, CreateOutBox
from app.models import Outbox
from datetime import datetime as dt, timezone


class OutBoxRepository(AsyncOutBoxRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _to_dto(m: "Outbox") -> OutBoxOutPut:

        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return OutBoxOutPut(
            id=m.id,
            aggregate_type=m.aggregate_type,
            aggregate_id=m.aggregate_id,
            event_type=m.event_type,
            payload=m.payload,
            idempotency_key=m.idempotency_key if m.idempotency_key else None,
            processed=m.processed,
            processed_at=m.processed_at if m.processed_at else None,
            created_at=m.created_at,
            status=m.status,
            error=m.error
        )

    async def create_out_box(self, event: CreateOutBox) -> OutBoxOutPut:
        m = Outbox()
        m.aggregate_type = event.aggregate_type
        m.aggregate_id = event.aggregate_id
        m.status = event.status
        m.processed = event.processed
        m.created_at = dt.now(timezone.utc)
        m.event_type = event.event_type
        m.payload = event.payload

        self.db.add(m)
        await self.db.flush()  # отправляем INSERT
        await self.db.refresh(m)  # обновляем объект из БД, теперь есть id

        return self._to_dto(m)

    async def create_out_box_many(self, events: CreateOutBoxList) -> List[Optional[OutBoxOutPut]]:
        if events is None:
            return []

        objs = []
        for e in events.events:
            obj = Outbox(
                aggregate_type=e.aggregate_type,
                aggregate_id=e.aggregate_id,
                status=e.status,
                processed=e.processed,
                created_at=dt.now(timezone.utc),
                event_type=e.event_type,
                payload=e.payload,
            )
            objs.append(obj)

        self.db.add_all(objs)
        await self.db.flush()  # получаем id всех объектов

        return [self._to_dto(m) for m in objs]
