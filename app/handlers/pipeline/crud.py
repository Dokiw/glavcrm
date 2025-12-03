import uuid
from typing import Optional

from app.handlers.pipeline.interfaces import AsyncDepartmentRepository, AsyncPipelineService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from app.handlers.pipeline.schemas import output_department, create_department, update_department, \
    output_pipeline_stage, create_pipeline_stage, update_pipeline_stage, settings_pipeline_stage
from app.models.performance import DepartmentPipeline, PipelineStage


class DepartmentRepository(AsyncDepartmentRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _to_dto(self, m: "DepartmentPipeline") -> output_department:
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return output_department(
            id=m.id,
            name=m.name,
            department_id=str(m.department_id),
            is_active=m.is_active,
            created_at=m.created_at
        )

    async def create_department(self, depart_data: create_department) -> output_department:
        m = DepartmentPipeline()
        m.department_id = uuid.uuid4()
        m.name = depart_data.name
        m.is_active = True

        self.db.add(m)
        await self.db.flush()
        return await self._to_dto(m) if m else None

    async def update_department(self, depart_data: update_department) -> Optional[output_department]:
        stmt = (
            update(DepartmentPipeline)
            .where(DepartmentPipeline.id == depart_data.id)
            .values(name=depart_data.name, is_active=depart_data.is_active)
            .returning(DepartmentPipeline)
        )
        result = await self.db.execute(stmt)
        result = result.scalar()
        return await self._to_dto(result) if result else None

    async def get_department_by_id(self, id: int) -> Optional[output_department]:
        result = await self.db.get(DepartmentPipeline, id)
        return await self._to_dto(result) if result else None

    async def delete_department_by_id(self, id: int) -> Optional[output_department]:
        # 1. Получаем объект
        result = await self.db.get(DepartmentPipeline, id)
        if not result:
            return None  # ничего не найдено

        # 2. Преобразуем в DTO перед удалением
        dto = await self._to_dto(result)  # обязательно await, если _to_dto async

        # 3. Удаляем объект
        await self.db.delete(result)
        await self.db.commit()  # если используешь async session, commit обязателен

        return dto


class PipelineRepository(AsyncPipelineService):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _to_dto(self, m: "PipelineStage") -> output_pipeline_stage:
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return output_pipeline_stage(
            id=m.id,
            pipeline_id=m.pipeline_id,
            name=m.name,
            position=m.position,
            meta_data=m.meta_data,
        )

    async def create_pipeline_stage(self, pipeline_data: create_pipeline_stage,
                                    settings: settings_pipeline_stage) -> output_pipeline_stage:
        m = PipelineStage()
        m.name = pipeline_data.name
        m.pipeline_id = pipeline_data.pipeline_id
        m.position = pipeline_data.position
        m.meta_data = pipeline_data.meta_data

        self.db.add(m)
        await self.db.flush()
        return await self._to_dto(m) if m else None

    async def update_pipeline_stage(self, pipeline_data: update_pipeline_stage, settings: settings_pipeline_stage) -> \
            Optional[output_pipeline_stage]:
        stmt = (
            update(PipelineStage)
            .where(PipelineStage.id == pipeline_data.id)
            .values(pipeline_id=pipeline_data.pipeline_id,
                    nam=pipeline_data.name,
                    position=pipeline_data.position,
                    meta_data=pipeline_data.meta_data
                    )
            .returning(PipelineStage)
        )
        result = await self.db.execute(stmt)
        result = result.scalar()
        return await self._to_dto(result) if result else None

    async def get_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        result = await self.db.get(PipelineStage, id)
        return await self._to_dto(result) if result else None

    async def delete_pipeline_stage_by_id(self, id: int) -> Optional[output_pipeline_stage]:
        obj = await self.db.get(PipelineStage, id)
        if not obj:
            return None

        await self.db.delete(obj)
        await self.db.flush()
        return await self._to_dto(obj) if obj else None

    async def next_pipeline_stage_by_current_id(self, id: int) -> Optional[output_pipeline_stage]:
        current_pipeline_stage = await self.db.get(PipelineStage, id)

        if current_pipeline_stage is None:
            return None

        stmt = (
            select(PipelineStage)
            .where(
                PipelineStage.pipeline_id == current_pipeline_stage.pipeline_id,
                PipelineStage.position > current_pipeline_stage.position
            )
            .order_by(PipelineStage.position.asc())
            .limit(1)
        )

        result = await self.db.execute(stmt)
        next_stage = result.scalar_one_or_none()

        return await self._to_dto(next_stage) if next_stage else None

    async def prev_pipeline_stage_by_current_id(self, id: int) -> Optional[output_pipeline_stage]:
        current_pipeline_stage = await self.db.get(PipelineStage, id)

        if current_pipeline_stage is None:
            return None

        stmt = (
            select(PipelineStage)
            .where(
                PipelineStage.pipeline_id == current_pipeline_stage.pipeline_id,
                PipelineStage.position < current_pipeline_stage.position
            )
            .order_by(PipelineStage.position.asc())
            .limit(1)
        )

        result = await self.db.execute(stmt)
        next_stage = result.scalar_one_or_none()

        return await self._to_dto(next_stage) if next_stage else None
