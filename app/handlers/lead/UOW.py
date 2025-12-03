from abc import ABC
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.lead.crud import MasterLeadRepository, SubLeadRepository
from app.handlers.lead.interfaces import AsyncMasterLeadRepository, AsyncSubLeadRepository


class SqlAlchemyUnitOfWorkMasterLead(IUnitOfWork[AsyncMasterLeadRepository]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self._master_lead_repo: Optional[AsyncMasterLeadRepository] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkMasterLead":
        self._session = self.session_factory()
        self._master_lead_repo = MasterLeadRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncMasterLeadRepository:
        return self._master_lead_repo

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class SqlAlchemyUnitOfWorkSubLead(IUnitOfWork[AsyncSubLeadRepository]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self._sub_lead_repo: Optional[AsyncSubLeadRepository] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkSubLead":
        self._session = self.session_factory()
        self._sub_lead_repo = SubLeadRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncSubLeadRepository:
        return self._sub_lead_repo

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
