from typing import Optional, List

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.task.interfaces import AsyncTaskService, AsyncTaskRepository
from app.handlers.task.schemas import CreateTask, UpdateTask, OutTask
from app.method.decorator import transactional


class TaskService(AsyncTaskService):

    def __init__(self, uow: IUnitOfWork[AsyncTaskRepository]):
        self.uow = uow

    @transactional()
    async def get_task_by_id(self, task_id: int) -> Optional[OutTask]:
        return await self.uow.repo.get_task_by_id(task_id)

    @transactional()
    async def create_task(self, data: CreateTask) -> OutTask:
        if data.sub_lead_id == 0:
            data.sub_lead_id = None
        return await self.uow.repo.create_task(data)

    @transactional()
    async def update_task(self, data: UpdateTask) -> Optional[OutTask]:
        return await self.uow.repo.update_task(data)

    @transactional()
    async def delete_task_by_id(self, task_id: int) -> OutTask:
        return await self.uow.repo.delete_task_by_id(task_id)

    @transactional()
    async def get_task_by_user_id(self, user_id: int):
        ...

    @transactional()
    async def get_task_by_sub_lead_id(self, sub_lead_id: int) -> Optional[List[OutTask]]:
        return await self.uow.repo.get_task_by_sub_lead_id(sub_lead_id)
