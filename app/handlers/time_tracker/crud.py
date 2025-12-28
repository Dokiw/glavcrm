from datetime import datetime as dt, timezone as tz
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.task.interfaces import AsyncTaskRepository
from app.handlers.task.schemas import CreateTask, UpdateTask, OutTask
from app.handlers.time_tracker.interfaces import AsyncTimeTrackerRepository
from app.handlers.time_tracker.schemas import OutTimeTracker, CreateTimeTracker, UpdateTimeTracker
from app.models import Task
from app.models.time_tracker import TimeTracker


class TimeTrackerRepository(AsyncTimeTrackerRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _to_dto(self, m: "TimeTracker") -> OutTimeTracker:
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return OutTimeTracker(
            id=m.id,
            task_id=m.task_id,
            operating=m.operating,
            payment=m.payment,
            created_at=m.created_at,
            status=m.status,
            completed_at=m.completed_at,
            meta_data=m.meta_data,
        )

    async def get_time_tracker_by_id(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        res = await self.db.get(TimeTracker, time_tracker_id)
        return await self._to_dto(res) if res else None

    async def get_time_tracker_by_task_id(self, task_id: int) -> Optional[OutTimeTracker]:
        stmt = (
            select(TimeTracker)
            .where(TimeTracker.task_id == task_id)
            .order_by(TimeTracker.created_at.desc())
        )

        tracker: Optional[TimeTracker] = await self.db.scalars(stmt).first()

        return await self._to_dto(tracker) if tracker else None

    async def create_time_tracker(self, data: CreateTimeTracker) -> OutTimeTracker:
        m = TimeTracker()
        m.created_at = dt.now(tz.utc)
        m.meta_data = data.meta_data
        m.status = data.status if data.status else "Created"
        m.task_id = data.task_id
        m.completed_at = None
        m.payment = data.payment
        m.operating = 0

        self.db.add(m)
        await self.db.flush()
        await self.db.refresh(m)

        return await self._to_dto(m)

    async def update_time_tracker(self, data: UpdateTimeTracker) -> Optional[OutTimeTracker]:
        values = data.model_dump(exclude_unset=True, exclude_none=True)
        values.pop("id", None)

        stmt = (
            update(TimeTracker)
            .where(
                TimeTracker.id == data.id
            )
            .values(**values)
            .returning(TimeTracker)
        )

        result = await self.db.execute(stmt)
        result = result.scalar()
        return await self._to_dto(result) if result else None

    async def delete_time_tracker(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        obj = await self.db.get(TimeTracker, time_tracker_id)
        if obj is None:
            return None

        dto = await self._to_dto(obj)

        await self.db.delete(obj)

        return dto
