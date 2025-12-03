from typing import Optional

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.lead.interfaces import AsyncMasterLeadService, AsyncSubLeadService, AsyncMasterLeadRepository, \
    AsyncSubLeadRepository
from app.handlers.lead.schemas import MasterLeadCreate, MasterLeadOut, MasterLeadUpdate, SubLeadCreate, SubLeadOut, \
    SubLeadUpdate, ListSubLeadOut
from app.handlers.pipeline.interfaces import AsyncPipelineService
from app.handlers.task.interfaces import AsyncOutBoxService
from app.method.decorator import transactional


class MasterLeadService(AsyncMasterLeadService):

    def __init__(self, uow: IUnitOfWork[AsyncMasterLeadRepository], event_outbox: AsyncOutBoxService):
        self.uow = uow,
        self.event_outbox = event_outbox

    @transactional()
    async def create_master_lead(self, data_create: MasterLeadCreate) -> MasterLeadOut:
        return await self.uow.repo.create_master_lead(data_create)

    @transactional()
    async def update_master_lead(self, data_update: MasterLeadUpdate) -> Optional[MasterLeadOut]:
        return await self.uow.repo.update_master_lead(data_update)

    @transactional()
    async def get_master_lead_by_id(self, id: int) -> Optional[MasterLeadOut]:
        return await self.uow.repo.get_master_lead_by_id(id)

    @transactional()
    async def delete_master_lead(self, id: int) -> Optional[MasterLeadOut]:
        return await self.uow.repo.delete_master_lead(id)


class SubLeadService(AsyncSubLeadService):

    def __init__(self, uow: IUnitOfWork[AsyncSubLeadRepository], pipeline_service: AsyncPipelineService,
                 event_outbox: AsyncOutBoxService):
        self.uow = uow
        self.pipeline_service = pipeline_service
        self.event_outbox = event_outbox

    @transactional()
    async def create_sub_lead(self, data_create: SubLeadCreate) -> SubLeadOut:
        return await self.uow.repo.create_sub_lead(data_create)

    @transactional()
    async def update_sub_lead(self, data_update: SubLeadUpdate) -> Optional[SubLeadOut]:
        return await self.uow.repo.update_sub_lead(data_update)

    @transactional()
    async def get_sub_lead_by_id(self, id: int) -> Optional[SubLeadOut]:
        return await self.uow.repo.get_sub_lead_by_id(id)

    @transactional()
    async def delete_sub_lead(self, id: int) -> Optional[SubLeadOut]:
        return await self.uow.repo.delete_sub_lead(id)

    @transactional()
    async def next_sub_lead_stage(self, sub_lead_id: int) -> Optional[SubLeadOut]:
        current_sub_lead = await self.get_sub_lead_by_id(sub_lead_id)

        if current_sub_lead.status == "Closed":
            return current_sub_lead

        current_pipeline = await self.pipeline_service.get_pipeline_stage_by_id(current_sub_lead.stage_id)

        next_stage = await self.pipeline_service.next_pipeline_stage_by_current_id(current_pipeline.id)

        if not next_stage:
            return None  # значит стадия последняя

        data_create = SubLeadCreate(
            master_lead_id=current_sub_lead.master_lead_id,
            department_id=current_sub_lead.department_id,
            pipeline_id=current_pipeline.pipeline_id,
            stage_id=next_stage.id,
            status="Created",
            meta_data=current_sub_lead.meta_data,
        )
        res = await self.create_sub_lead(data_create)

        data_update = SubLeadUpdate(
            id=current_sub_lead.id,
            status="Closed"
        )

        await self.uow.repo.update_sub_lead(data_update)

        return res

    @transactional()
    async def move_sub_lead_stage(self, sub_lead_id: int, to_stage_id: int) -> Optional[SubLeadOut]:
        current_sub_lead = await self.get_sub_lead_by_id(sub_lead_id)
        move_pipeline = await self.pipeline_service.get_pipeline_stage_by_id(to_stage_id)

        if not move_pipeline:
            return None  # значит стадия последняя

        data_create = SubLeadCreate(
            master_lead_id=current_sub_lead.master_lead_id,
            department_id=current_sub_lead.department_id,
            pipeline_id=move_pipeline.pipeline_id,
            stage_id=move_pipeline.id,
            status="Created",
            meta_data=current_sub_lead.meta_data,
        )
        res = await self.create_sub_lead(data_create)

        data_update = SubLeadUpdate(
            id=current_sub_lead.id,
            status="Closed"
        )

        await self.uow.repo.update_sub_lead(data_update)

        return res

    @transactional()
    async def prev_sub_lead_stage(self, sub_lead_id: int) -> Optional[SubLeadOut]:
        current_sub_lead = await self.get_sub_lead_by_id(sub_lead_id)
        prev_pipeline = await self.pipeline_service.prev_pipeline_stage_by_current_id(current_sub_lead.stage_id)

        if not prev_pipeline:
            return None  # значит стадия последняя

        data_create = SubLeadCreate(
            master_lead_id=current_sub_lead.master_lead_id,
            department_id=current_sub_lead.department_id,
            pipeline_id=prev_pipeline.pipeline_id,
            stage_id=prev_pipeline.id,
            status="Created",
            meta_data=current_sub_lead.meta_data,
        )
        res = await self.create_sub_lead(data_create)

        data_update = SubLeadUpdate(
            id=current_sub_lead.id,
            status="Closed"
        )

        await self.uow.repo.update_sub_lead(data_update)

        return res

    @transactional()
    async def list_sub_lead(self, offset: int, limit: int) -> Optional[ListSubLeadOut]:
        return await self.uow.repo.list_sub_lead(offset, limit)
