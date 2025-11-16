from typing import Protocol, Optional

from app.handlers.pipeline.schemas import create_department, output_department, update_department, \
    create_pipeline_stage, output_pipeline_stage, update_pipeline_stage, settings_pipeline_stage


class AsyncDepartmentRepository(Protocol):

    async def create_department(self, depart_data: create_department) -> output_department:
        ...

    async def update_department(self, depart_data: update_department) -> Optional[output_department]:
        ...

    async def get_department_by_id(self, id: int) -> Optional[output_department]:
        ...

    async def delete_department_by_id(self, id: int) -> Optional[output_department]:
        ...


class AsyncPipelineRepository(Protocol):

    async def create_pipeline_stage(self, pipeline_data: create_pipeline_stage) -> output_pipeline_stage:
        ...

    async def update_pipeline_stage(self, pipeline_data: update_pipeline_stage) -> Optional[output_pipeline_stage]:
        ...

    async def get_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        ...

    async def delete_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        ...


class AsyncDepartmentService(Protocol):

    async def create_department(self, depart_data: create_department) -> output_department:
        ...

    async def update_department(self, depart_data: update_department) -> Optional[output_department]:
        ...

    async def get_department_by_id(self, id: int) -> Optional[output_department]:
        ...

    async def delete_department_by_id(self, id: int) -> Optional[output_department]:
        ...


class AsyncPipelineService(Protocol):

    async def create_pipeline_stage(self, pipeline_data: create_pipeline_stage, settings: settings_pipeline_stage) -> (
            output_pipeline_stage):
        ...

    async def update_pipeline_stage(self, pipeline_data: update_pipeline_stage, settings: settings_pipeline_stage) -> (
            Optional)[output_pipeline_stage]:
        ...

    async def get_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        ...

    async def delete_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        ...
