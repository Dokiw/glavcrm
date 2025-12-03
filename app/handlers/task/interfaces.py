from typing import Protocol, Optional

from app.handlers.pipeline.schemas import create_department, output_department, update_department, \
    create_pipeline_stage, output_pipeline_stage, update_pipeline_stage, settings_pipeline_stage


class AsyncOutBoxRepository(Protocol):

    async def create_out_box(self, event: dict):
        ...

    async def create_out_box_many(self, events: list[dict]):
        ...


class AsyncOutBoxService(Protocol):

    async def create_out_box(self, event: dict):
        ...

    async def create_out_box_many(self, events: list[dict]):
        ...
