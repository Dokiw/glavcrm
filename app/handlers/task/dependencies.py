from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWork
from app.db.session import get_db
from app.handlers.task.UOW import SqlAlchemyUnitOfWorkTask
from app.handlers.task.interfaces import AsyncTaskRepository, AsyncTaskService
from app.handlers.task.service import TaskService


async def get_uow(db: AsyncSession = Depends(get_db)) -> AsyncGenerator[IUnitOfWork[AsyncTaskRepository], None]:
    uow = SqlAlchemyUnitOfWorkTask(lambda: db)  # тут session_factory — обычная функция
    async with uow:
        yield uow


async def get_task_service(
        uow: IUnitOfWork[AsyncTaskRepository] = Depends(get_uow)
) -> AsyncTaskService:
    return TaskService(uow=uow)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]

