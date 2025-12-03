# app/handlers/session/dependencies.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.db.session import get_db
from app.handlers.OutBoxTask.UOW import SqlAlchemyUnitOfWorkOutBox
from app.handlers.OutBoxTask.interfaces import AsyncOutBoxRepository, AsyncOutBoxService
from app.handlers.OutBoxTask.service import OutBoxService


# фабрика UnitOfWork
async def get_uow(db: AsyncSession = Depends(get_db)) -> IUnitOfWork[AsyncOutBoxRepository]:
    async with SqlAlchemyUnitOfWorkOutBox(lambda: db) as uow:
        yield uow


# фабрика сервиса сессий
def get_session_service(
        uow: IUnitOfWork[AsyncOutBoxRepository] = Depends(get_uow)
) -> AsyncOutBoxService:
    return OutBoxService(uow=uow)


# alias для роутов
OutBoxDep = Annotated[OutBoxService, Depends(get_session_service)]

