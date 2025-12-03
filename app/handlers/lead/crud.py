from datetime import datetime as dt, timezone
from typing import Optional

from sqlalchemy import update, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.lead.interfaces import AsyncMasterLeadRepository, AsyncSubLeadRepository
from app.handlers.lead.schemas import MasterLeadOut, MasterLeadCreate, \
    MasterLeadUpdate, SubLeadCreate, SubLeadOut, SubLeadUpdate, ListSubLeadOut
from app.models import MasterLead, SubLead


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
            sub_leads=[],
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
        await self.db.flush()  # отправляем INSERT
        await self.db.refresh(m)  # обновляем объект из БД, теперь есть id

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

        await self.db.flush()  # выполняет INSERT
        await self.db.refresh(m)  # запрашивает реальные значения

        return await self._to_dto(m)

    async def update_sub_lead(self, data_update: SubLeadUpdate) -> Optional[SubLeadOut]:

        values = data_update.model_dump(exclude_unset=True, exclude_none=True)
        values.pop("id", None)

        stmt = (
            update(SubLead)
            .where(SubLead.id == data_update.id)
            .values(**values)
            .returning(SubLead)
        )

        result = await self.db.execute(stmt)
        row = result.scalar_one_or_none()

        return await self._to_dto(row)

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

    async def list_sub_lead(self, offset: int, limit: int = 50) -> Optional[ListSubLeadOut]:

        stmt = (
            select(SubLead)
            .offset(offset)
            .limit(limit)
        )

        count_stmt = select(func.count()).select_from(SubLead)

        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        total = await self.db.execute(count_stmt)
        total = total.scalar_one()

        # Формируем ответ
        return ListSubLeadOut(
            data_sub_lead=rows,
            total=total,
            offset=offset,
            limit=limit
        )

    async def list_sub_lead_from_master_lead_id(self, master_lead_id: int, offset: int, limit: int = 50) -> Optional[
        ListSubLeadOut]:

        stmt = (
            select(SubLead)
            .where(SubLead.master_lead_id == master_lead_id)
            .offset(offset)
            .limit(limit)
        )

        count_stmt = select(func.count()).select_from(SubLead).where(SubLead.master_lead_id == master_lead_id)

        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        total = await self.db.execute(count_stmt)
        total = total.scalar_one()

        # Формируем ответ
        return ListSubLeadOut(
            data_sub_lead=rows,
            total=total,
            offset=offset,
            limit=limit
        )

    async def list_sub_lead_from_department_pipeline_id(self, depart_pipeline_id: int, offset: int, limit: int = 50) -> \
            Optional[
                ListSubLeadOut]:

        stmt = (
            select(SubLead)
            .where(SubLead.pipeline_id == depart_pipeline_id)
            .offset(offset)
            .limit(limit)
        )

        count_stmt = select(func.count()).select_from(SubLead).where(SubLead.pipeline_id == depart_pipeline_id)

        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        total = await self.db.execute(count_stmt)
        total = total.scalar_one()

        return ListSubLeadOut(
            data_sub_lead=rows,
            total=total,
            offset=offset,
            limit=limit
        )
