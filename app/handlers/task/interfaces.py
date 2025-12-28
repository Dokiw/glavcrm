from typing import Protocol, Optional, List

from app.handlers.task.schemas import CreateTask, UpdateTask, OutTask


class AsyncTaskRepository(Protocol):

    async def get_task_by_id(self, task_id: int) -> Optional[OutTask]:
        ...

    async def create_task(self, data: CreateTask) -> OutTask:
        ...

    async def update_task(self, data: UpdateTask) -> Optional[OutTask]:
        ...

    async def delete_task_by_id(self, task_id: int) -> OutTask:
        ...

    async def get_task_by_sub_lead_id(self, sub_lead_id: int) -> Optional[List[OutTask]]:
        ...


class AsyncTaskService(Protocol):

    async def get_task_by_id(self, task_id: int) -> Optional[OutTask]:
        ...

    async def create_task(self, data: CreateTask) -> OutTask:
        ...

    async def update_task(self, data: UpdateTask) -> Optional[OutTask]:
        ...

    async def delete_task_by_id(self, task_id: int) -> OutTask:
        ...

    async def get_task_by_user_id(self, user_id: int):
        ...

    async def get_task_by_sub_lead_id(self, sub_lead_id: int) -> Optional[List[OutTask]]:
        ...
