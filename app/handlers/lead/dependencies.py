# app/handlers/session/dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.db.session import get_db

from app.handlers.lead.UOW import SqlAlchemyUnitOfWorkMasterLead, SqlAlchemyUnitOfWorkSubLead
from app.handlers.lead.interfaces import AsyncMasterLeadService, AsyncSubLeadService, AsyncMasterLeadRepository, \
    AsyncSubLeadRepository
from app.handlers.lead.service import MasterLeadService, SubLeadService
from app.handlers.pipeline.dependencies import PipelineServiceDep
from app.handlers.task.dependencies import OutBoxDep


# фабрика UnitOfWork
async def get_uow(db: AsyncSession = Depends(get_db)) -> IUnitOfWork[AsyncMasterLeadRepository]:
    async with SqlAlchemyUnitOfWorkMasterLead(lambda: db) as uow:
        yield uow


# фабрика сервиса сессий
def get_session_service(
        event_outbox: OutBoxDep,
        uow: IUnitOfWork[AsyncMasterLeadRepository] = Depends(get_uow)
) -> AsyncMasterLeadService:
    return MasterLeadService(uow=uow, event_outbox=event_outbox)


# alias для роутов
MasterLeadServiceDep = Annotated[MasterLeadService, Depends(get_session_service)]


async def get_uow_s(db: AsyncSession = Depends(get_db)) -> IUnitOfWork[AsyncSubLeadRepository]:
    async with SqlAlchemyUnitOfWorkSubLead(lambda: db) as uow:
        yield uow


# фабрика сервиса сессий
def get_session_service_s(
        pipeline_service: PipelineServiceDep,
        event_outbox: OutBoxDep,
        uow: IUnitOfWork[AsyncSubLeadRepository] = Depends(get_uow_s)
) -> AsyncSubLeadService:
    return SubLeadService(uow=uow,pipeline_service=pipeline_service,event_outbox=event_outbox)


# alias для роутов
SubLeadServiceDep = Annotated[SubLeadService, Depends(get_session_service_s)]
