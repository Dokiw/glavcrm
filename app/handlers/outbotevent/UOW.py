from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.outbotevent.crud import OutBoxRepository
from app.handlers.outbotevent.interfaces import AsyncOutBoxRepository


class SqlAlchemyUnitOfWorkOutBox(IUnitOfWork[AsyncOutBoxRepository]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self._out_box_repo: Optional[AsyncOutBoxRepository] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkOutBox":
        self._session = self.session_factory()
        self._out_box_repo = OutBoxRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncOutBoxRepository:
        return self._out_box_repo

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()