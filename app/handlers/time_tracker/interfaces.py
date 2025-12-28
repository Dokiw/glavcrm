from typing import Protocol, Optional

from app.handlers.time_tracker.schemas import CreateTimeTracker, UpdateTimeTracker, OutTimeTracker


class AsyncTimeTrackerRepository(Protocol):

    async def get_time_tracker_by_id(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        ...

    async def get_time_tracker_by_task_id(self, task_id: int) -> Optional[OutTimeTracker]:
        ...

    async def create_time_tracker(self, data: CreateTimeTracker) -> OutTimeTracker:
        ...

    async def update_time_tracker(self, data: UpdateTimeTracker) -> Optional[OutTimeTracker]:
        ...

    async def delete_time_tracker(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        ...


class AsyncTimeTrackerService(Protocol):

    async def get_time_tracker_by_id(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        ...

    async def get_time_tracker_by_task_id(self, task_id: int) -> Optional[OutTimeTracker]:
        ...

    async def create_time_tracker(self, data: CreateTimeTracker) -> OutTimeTracker:
        ...

    async def update_time_tracker(self, data: UpdateTimeTracker) -> Optional[OutTimeTracker]:
        ...

    async def delete_time_tracker(self, time_tracker_id: int) -> Optional[OutTimeTracker]:
        ...




