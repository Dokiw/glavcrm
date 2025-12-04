from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.db.session import get_db
from app.handlers.subleadevent.UOW import SqlAlchemyUnitOfWorkSubLeadEvent
from app.handlers.subleadevent.interfaces import AsyncSubLeadEventRepo, AsyncSubLeadEventService
from app.handlers.subleadevent.service import SubLeadEventService


async def get_uow(db: AsyncSession = Depends(get_db)) -> AsyncGenerator[IUnitOfWork[AsyncSubLeadEventRepo], None]:
    uow = SqlAlchemyUnitOfWorkSubLeadEvent(lambda: db)  # тут session_factory — обычная функция
    async with uow:
        yield uow


async def get_pipeline_service(
        uow: IUnitOfWork[AsyncSubLeadEventRepo] = Depends(get_uow)
) -> AsyncSubLeadEventService:
    return SubLeadEventService(uow=uow)


SubLeadEventServiceDep = Annotated[SubLeadEventService, Depends(get_pipeline_service)]

