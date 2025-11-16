from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.abs.unit_of_work import IUnitOfWorkPipelineStage, IUnitOfWorkDepart
from app.db.session import get_db
from app.handlers.pipeline.UOW import SqlAlchemyUnitOfWorkPipeline, SqlAlchemyUnitOfWorkDepart
from app.handlers.pipeline.interfaces import AsyncPipelineService, AsyncDepartmentService
from app.handlers.pipeline.service import PipelineService, DepartmentService


async def get_uow(db: AsyncSession = Depends(get_db)) -> AsyncGenerator[IUnitOfWorkPipelineStage, None]:
    uow = SqlAlchemyUnitOfWorkPipeline(lambda: db)  # тут session_factory — обычная функция
    async with uow:
        yield uow


async def get_pipeline_service(
        uow: IUnitOfWorkPipelineStage = Depends(get_uow)
) -> AsyncPipelineService:
    return PipelineService(uow=uow)


PipelineServiceDep = Annotated[PipelineService, Depends(get_pipeline_service)]


async def get_uow_depart(db: AsyncSession = Depends(get_db)) -> AsyncGenerator[IUnitOfWorkDepart, None]:
    uow = SqlAlchemyUnitOfWorkDepart(lambda: db)  # тут session_factory — обычная функция
    async with uow:
        yield uow


async def get_depart_service(
        uow: IUnitOfWorkDepart = Depends(get_uow_depart)
) -> AsyncDepartmentService:
    return DepartmentService(uow=uow)

DepartServiceDep = Annotated[DepartmentService, Depends(get_depart_service)]