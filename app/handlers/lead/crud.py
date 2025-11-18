from datetime import datetime as dt, timezone

import time
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional, List

from app.handlers.lead.interfaces import AsyncMasterLeadRepository, AsyncSubLeadRepository
from app.handlers.lead.schemas import MasterLeadOut, MasterLeadCreate, \
    MasterLeadUpdate, SubLeadCreate, SubLeadOut, SubLeadUpdate
from app.models import MasterLead, SubLead

from sqlalchemy import update


class MasterLeadRepository(AsyncMasterLeadRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _to_dto(self, m: "MasterLead") -> MasterLeadOut:
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return MasterLeadOut(
            id=m.id,
            title=m.title,
            payload=m.payload,
            status=m.status,
            completion_rule=m.completion_rule,
            created_by=m.created_by,
            created_at=m.created_at,
            closed_at=m.closed_at,
            result=m.result,
            version=m.version,
            contact_id=m.contact_id,
            sub_leads=m.sub_leads,
        )

    async def create_master_lead(self, data_create: MasterLeadCreate) -> MasterLeadOut:
        m = MasterLead()
        m.title = data_create.title
        m.payload = data_create.payload
        m.status = data_create.status
        m.completion_rule = data_create.completion_rule
        m.created_by = data_create.created_by
        m.created_at = dt.now(timezone.utc)
        m.version = 1

        self.db.add(m)
        return await self._to_dto(m)

    async def update_master_lead(self, data_update: MasterLeadUpdate) -> Optional[MasterLeadOut]:

        stmt = (
            update(MasterLead)
            .where(MasterLead.id == data_update.id)
            .values(
                title=data_update.title,
                payload=data_update.payload,
                status=data_update.status,
                completion_rule=data_update.completion_rule,
                closed_at=data_update.closed_at,
                result=data_update.result,
                version=data_update.version,
                contact_id=data_update.contact_id,
                sub_leads=data_update.sub_leads
            )
        )

        result = await self.db.execute(stmt)
        result = result.scalar_one_or_none()
        return await self._to_dto(result)

    async def get_master_lead_by_id(self, id: int) -> Optional[MasterLeadOut]:
        return await self.db.get(MasterLead, id)

    async def delete_master_lead(self, id: int) -> Optional[MasterLeadOut]:
        obj = await self.db.get(MasterLead, id)
        if obj is None:
            return None

        dto = await self._to_dto(obj)

        await self.db.delete(obj)
        await self.db.commit()

        return dto


class SubLeadRepository(AsyncSubLeadRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _to_dto(self, m: "SubLead") -> SubLeadOut:
        if m is None:
            raise TypeError("_to_dto получил None")
        if isinstance(m, type):
            raise TypeError(f"_to_dto получил класс {m!r}, ожидается экземпляр Session")

        return SubLeadOut(
            id=m.id,
            master_lead_id=m.master_lead_id,
            department_id=m.department_id,
            pipeline_id=m.pipeline_id,
            stage_id=m.stage_id,
            status=m.status,
            meta_data=m.meta_data,
            version=m.version,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def create_sub_lead(self, data_create: SubLeadCreate) -> SubLeadOut:
        m = SubLead()
        m.master_lead_id = data_create.master_lead_id
        m.department_id = data_create.department_id
        m.pipeline_id = data_create.pipeline_id
        m.stage_id = data_create.stage_id
        m.status = data_create.status
        m.meta_data = data_create.meta_data

        self.db.add(m)
        return await self._to_dto(m)

    async def update_sub_lead(self, data_update: SubLeadUpdate) -> Optional[SubLeadOut]:
        stmt = (
            update(SubLead)
            .where(SubLead.id == data_update.id)
            .values(
                master_lead_id=data_update.master_lead_id,
                department_id=data_update.department_id,
                pipeline_id=data_update.pipeline_id,
                stage_id=data_update.stage_id,
                status=data_update.status,
                meta_data=data_update.meta_data,
                version=data_update.version,
            )
        )

        result = await self.db.execute(stmt)
        result = result.scalar_one_or_none()
        return await self._to_dto(result)

    async def get_sub_lead_by_id(self, id: int) -> Optional[SubLeadOut]:
        return await self.db.get(SubLead, id)

    async def delete_sub_lead(self, id: int) -> Optional[SubLeadOut]:
        obj = await self.db.get(SubLead, id)
        if obj is None:
            return None

        dto = await self._to_dto(obj)

        await self.db.delete(obj)
        await self.db.commit()

        return dto
