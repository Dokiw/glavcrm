from typing import Protocol, Optional, List

from app.handlers.pipeline.schemas import create_department, output_department, update_department, \
    create_pipeline_stage, output_pipeline_stage, update_pipeline_stage, settings_pipeline_stage
from app.handlers.task.schemas import CreateOutBox, CreateOutBoxList, OutBoxOutPut


class AsyncOutBoxRepository(Protocol):

    async def create_out_box(self, event: CreateOutBox) -> OutBoxOutPut:
        ...

    async def create_out_box_many(self, events: CreateOutBoxList) -> List[Optional[OutBoxOutPut]]:
        ...


class AsyncOutBoxService(Protocol):

    async def create_out_box(self, event: CreateOutBox) -> OutBoxOutPut:
        ...

    async def create_out_box_many(self, events: CreateOutBoxList) -> List[Optional[OutBoxOutPut]]:
        ...
