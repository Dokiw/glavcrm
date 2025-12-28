from typing import Optional, List

from app.core.abs.unit_of_work import IUnitOfWork
from app.handlers.task.interfaces import AsyncTaskService, AsyncTaskRepository
from app.handlers.task.schemas import CreateTask, UpdateTask, OutTask
from app.handlers.time_tracker.interfaces import AsyncTimeTrackerService, AsyncTimeTrackerRepository
from app.handlers.time_tracker.schemas import OutTimeTracker, CreateTimeTracker, UpdateTimeTracker
from app.method.decorator import transactional


class TimeTrackerService(AsyncTimeTrackerService):

    def __init__(self, uow: IUnitOfWork[AsyncTimeTrackerRepository]):
        self.uow = uow

    @transactional()
    async def get_time_tracker_by_id(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        return await self.uow.repo.get_time_tracker_by_id(time_tracker_id)

    @transactional()
    async def get_time_tracker_by_task_id(self, task_id: int) -> Optional[OutTimeTracker]:
        return await self.uow.repo.get_time_tracker_by_task_id(task_id)

    @transactional()
    async def create_time_tracker(self, data: CreateTimeTracker) -> OutTimeTracker:
        return await self.uow.repo.create_time_tracker(data)

    @transactional()
    async def update_time_tracker(self, data: UpdateTimeTracker) -> Optional[OutTimeTracker]:
        return await self.uow.repo.update_time_tracker(data)

    @transactional()
    async def delete_time_tracker(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        return await self.uow.repo.delete_time_tracker(time_tracker_id)
