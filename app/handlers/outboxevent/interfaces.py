from typing import Protocol, Optional, List

from app.handlers.outboxevent.schemas import CreateOutBox, CreateOutBoxList, OutBoxOutPut


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
