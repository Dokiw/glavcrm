from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.pipeline.crud import PipelineRepository, DepartmentRepository
from app.handlers.pipeline.interfaces import AsyncPipelineRepository, AsyncDepartmentRepository


class SqlAlchemyUnitOfWorkPipeline(IUnitOfWork[AsyncPipelineRepository]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.pipeline: Optional[AsyncPipelineRepository] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkPipeline":
        # Если session_factory асинхронная функция, нужно await
        self._session = self.session_factory()
        self.pipeline = PipelineRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncPipelineRepository:
        return self.pipeline

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class SqlAlchemyUnitOfWorkDepart(IUnitOfWork[AsyncDepartmentRepository]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.depart: Optional[AsyncDepartmentRepository] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkDepart":
        # Если session_factory асинхронная функция, нужно await
        self._session = self.session_factory()
        self.depart = DepartmentRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncDepartmentRepository:
        return self.depart

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


