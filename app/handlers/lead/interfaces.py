from typing import Protocol, List, Optional, Dict, Any

from app.handlers.lead.schemas import SubLeadCreate, SubLeadOut, SubLeadUpdate, MasterLeadOut, MasterLeadUpdate, \
    MasterLeadCreate


class AsyncSubLeadRepository(Protocol):

    async def create_sub_lead(self, data_create: SubLeadCreate) -> SubLeadOut:
        ...

    async def update_sub_lead(self, data_update: SubLeadUpdate) -> Optional[SubLeadOut]:
        ...

    async def get_sub_lead_by_id(self, id: int) -> Optional[SubLeadOut]:
        ...

    async def delete_sub_lead(self, id: int) -> Optional[SubLeadOut]:
        ...


class AsyncMasterLeadRepository(Protocol):

    async def create_master_lead(self, data_create: MasterLeadCreate) -> MasterLeadOut:
        ...

    async def update_master_lead(self, data_update: MasterLeadUpdate) -> Optional[MasterLeadOut]:
        ...

    async def get_master_lead_by_id(self, id: int) -> Optional[MasterLeadOut]:
        ...

    async def delete_master_lead(self, id: int) -> Optional[MasterLeadOut]:
        ...
