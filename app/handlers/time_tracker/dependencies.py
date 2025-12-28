from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.db.session import get_db
from app.handlers.time_tracker.UOW import SqlAlchemyUnitOfWorkTimeTracker
from app.handlers.time_tracker.interfaces import AsyncTimeTrackerRepository, AsyncTimeTrackerService
from app.handlers.time_tracker.service import TimeTrackerService


async def get_uow(db: AsyncSession = Depends(get_db)) -> AsyncGenerator[IUnitOfWork[AsyncTimeTrackerRepository], None]:
    uow = SqlAlchemyUnitOfWorkTimeTracker(lambda: db)  # тут session_factory — обычная функция
    async with uow:
        yield uow


async def get_time_tracker_service(
        uow: IUnitOfWork[AsyncTimeTrackerRepository] = Depends(get_uow)
) -> AsyncTimeTrackerService:
    return TimeTrackerService(uow=uow)


TimeTrackerServiceDep = Annotated[TimeTrackerService, Depends(get_time_tracker_service)]

