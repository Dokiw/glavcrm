from typing import Optional

from app.core.abs.unit_of_work import IUnitOfWorkDepart, IUnitOfWorkPipelineStage
from app.handlers.pipeline.interfaces import AsyncDepartmentService, AsyncPipelineService
from app.handlers.pipeline.schemas import create_department, output_department, update_department, \
    create_pipeline_stage, output_pipeline_stage, update_pipeline_stage, settings_pipeline_stage
from app.method.decorator import transactional


class DepartmentService(AsyncDepartmentService):

    def __init__(self, uow: IUnitOfWorkDepart):
        self.uow = uow

    @transactional()
    async def create_department(self, depart_data: create_department) -> output_department:
        return await self.uow.depart_repo.create_department(depart_data)

    @transactional()
    async def update_department(self, depart_data: update_department) -> Optional[output_department]:
        return await self.uow.depart_repo.update_department(depart_data)

    @transactional()
    async def get_department_by_id(self, id: int) -> Optional[output_department]:
        return await self.uow.depart_repo.get_department_by_id(id)

    @transactional()
    async def delete_department_by_id(self, id: int) -> Optional[output_department]:
        return await self.uow.depart_repo.delete_department_by_id(id)


class PipelineService(AsyncPipelineService):
    def __init__(self, uow: IUnitOfWorkPipelineStage):
        self.uow = uow

    @transactional()
    async def create_pipeline_stage(self, pipeline_data: create_pipeline_stage, settings: settings_pipeline_stage) -> (
            output_pipeline_stage):
        pipeline_data.meta_data = settings.model_dump(by_alias=True, exclude_none=True)
        return await self.uow.pipeline_repo.create_pipeline_stage(pipeline_data)

    @transactional()
    async def update_pipeline_stage(self, pipeline_data: update_pipeline_stage, settings: settings_pipeline_stage) -> (
            Optional[output_pipeline_stage]):
        pipeline_data.meta_data = settings.model_dump(by_alias=True, exclude_none=True)
        return await self.uow.pipeline_repo.update_pipeline_stage(pipeline_data)

    @transactional()
    async def get_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        return await self.uow.pipeline_repo.get_pipeline_stage_by_id(id)

    @transactional()
    async def delete_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        return await self.uow.pipeline_repo.get_pipeline_stage_by_id(id)
