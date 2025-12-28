from datetime import datetime as dt, timezone as tz
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.task.interfaces import AsyncTaskRepository
from app.handlers.task.schemas import CreateTask, UpdateTask, OutTask
from app.models import Task


class TaskRepository(AsyncTaskRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _to_dto(self, m: "Task") -> OutTask:
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return OutTask(
            id=m.id,
            sub_lead_id=m.sub_lead_id,
            assigned_to=m.assigned_to,
            title=m.title,
            description=m.description,
            status=m.status,
            due_date=m.due_date,
            meta_data=m.meta_data,
        )

    async def get_task_by_id(self, task_id: int) -> Optional[OutTask]:
        result = await self.db.get(Task, task_id)
        return await self._to_dto(result) if result else None

    async def create_task(self, data: CreateTask) -> OutTask:
        m = Task()
        m.created_at = dt.now(tz.utc)
        m.meta_data = data.meta_data
        m.status = data.status
        m.title = data.title
        m.due_date = data.due_date
        m.description = data.description
        m.sub_lead_id = data.sub_lead_id
        m.assigned_to = data.assigned_to

        self.db.add(m)
        await self.db.flush()
        await self.db.refresh(m)  # обновляем объект из БД, теперь есть id

        return await self._to_dto(m)

    async def update_task(self, data: UpdateTask) -> Optional[OutTask]:

        values = data.model_dump(exclude_unset=True, exclude_none=True)
        values.pop("id", None)

        stmt = (
            update(Task)
            .where(Task.id == Task.id)
            .values(**values)
            .returning(Task)
        )

        result = await self.db.execute(stmt)
        result = result.scalar()
        return await self._to_dto(result) if result else None

    async def delete_task_by_id(self, task_id: int) -> OutTask:
        obj = await self.db.get(Task, task_id)
        if obj is None:
            return None

        dto = await self._to_dto(obj)

        await self.db.delete(obj)

        return dto

    async def get_task_by_sub_lead_id(self, sub_lead_id: int) -> Optional[List[OutTask]]:
        stmt = (
            select(Task)
            .where(Task.sub_lead_id == sub_lead_id)
            .order_by(Task.created_at.desc())
        )

        result = await self.db.execute(stmt)
        result = result.scalars()
        return [await self._to_dto(res) if res else None for res in result]
