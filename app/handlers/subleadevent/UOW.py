from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.subleadevent.crud import SubLeadEventRepo
from app.handlers.subleadevent.interfaces import AsyncSubLeadEventRepo


class SqlAlchemyUnitOfWorkSubLeadEvent(IUnitOfWork[AsyncSubLeadEventRepo]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.sub_lead_event: Optional[AsyncSubLeadEventRepo] = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWorkSubLeadEvent":
        # Если session_factory асинхронная функция, нужно await
        self._session = self.session_factory()
        self.sub_lead_event = SubLeadEventRepo(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()  # автоматически сохраняем изменения
        else:
            await self.rollback()
        await self._session.close()

    @property
    def repo(self) -> AsyncSubLeadEventRepo:
        return self.sub_lead_event

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
