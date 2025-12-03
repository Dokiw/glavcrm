from typing import Protocol, List, Optional, Dict, Any

from app.handlers.lead.schemas import SubLeadCreate, SubLeadOut, SubLeadUpdate, MasterLeadOut, MasterLeadUpdate, \
    MasterLeadCreate, ListSubLeadOut


class AsyncSubLeadRepository(Protocol):

    async def create_sub_lead(self, data_create: SubLeadCreate) -> SubLeadOut:
        ...

    async def update_sub_lead(self, data_update: SubLeadUpdate) -> Optional[SubLeadOut]:
        ...

    async def get_sub_lead_by_id(self, id: int) -> Optional[SubLeadOut]:
        ...

    async def delete_sub_lead(self, id: int) -> Optional[SubLeadOut]:
        ...

    async def list_sub_lead(self, offset: int, limit: int) -> Optional[ListSubLeadOut]:
        ...

    async def list_sub_lead_from_master_lead_id(self, master_lead_id: int, offset: int, limit: int = 50) -> Optional[
        ListSubLeadOut]:
        ...

    async def list_sub_lead_from_department_pipeline_id(self, master_lead_id: int, offset: int, limit: int = 50) -> \
            Optional[
                ListSubLeadOut]:
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


class AsyncMasterLeadService(Protocol):

    async def create_master_lead(self, data_create: MasterLeadCreate) -> MasterLeadOut:
        ...

    async def update_master_lead(self, data_update: MasterLeadUpdate) -> Optional[MasterLeadOut]:
        ...

    async def get_master_lead_by_id(self, id: int) -> Optional[MasterLeadOut]:
        ...

    async def delete_master_lead(self, id: int) -> Optional[MasterLeadOut]:
        ...


class AsyncSubLeadService(Protocol):

    async def create_sub_lead(self, data_create: SubLeadCreate) -> SubLeadOut:
        ...

    async def update_sub_lead(self, data_update: SubLeadUpdate) -> Optional[SubLeadOut]:
        ...

    async def get_sub_lead_by_id(self, id: int) -> Optional[SubLeadOut]:
        ...

    async def delete_sub_lead(self, id: int) -> Optional[SubLeadOut]:
        ...

    async def next_sub_lead_stage(self, sub_lead_id: int) -> Optional[SubLeadOut]:
        ...

    async def move_sub_lead_stage(self, sub_lead_id: int, to_stage_id: int) -> Optional[SubLeadOut]:
        ...

    async def prev_sub_lead_stage(self, sub_lead_id: int) -> Optional[SubLeadOut]:
        ...

    async def list_sub_lead(self, offset: int, limit: int) -> Optional[ListSubLeadOut]:
        ...

    async def list_sub_lead_from_master_lead_id(self, master_lead_id: int, offset: int, limit: int = 50) -> Optional[
        ListSubLeadOut]:
        ...

    async def list_sub_lead_from_department_pipeline_id(self, master_lead_id: int, offset: int, limit: int = 50) -> \
            Optional[
                ListSubLeadOut]:
        ...
