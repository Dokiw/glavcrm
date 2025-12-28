from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.task.crud import TaskRepository
from app.handlers.task.interfaces import AsyncTaskRepository


class SqlAlchemyUnitOfWorkTask(IUnitOfWork[AsyncTaskRepository]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.task: Optional[AsyncTaskRepository] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkTask":
        # Если session_factory асинхронная функция, нужно await
        self._session = self.session_factory()
        self.task = TaskRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncTaskRepository:
        return self.task

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
