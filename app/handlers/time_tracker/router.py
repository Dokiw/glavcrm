from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from app.handlers.api_access_server.dependencies import ApiMainServiceDep
from app.handlers.api_access_server.interfaces import async_api_main_server
from app.handlers.api_access_server.schemas import CheckSessionAccessToken
from app.handlers.time_tracker.dependencies import TimeTrackerServiceDep
from app.handlers.time_tracker.schemas import OutTimeTracker, CreateTimeTracker, UpdateTimeTracker
from app.method.get_token import get_token

router_time_tracker = APIRouter(prefix="/TimeTracker", tags=["TimeTracker"])


@router_time_tracker.get("/")
async def hub():
    return HTTPException(200, 'Status - True')


@router_time_tracker.get("/{time_tracker_id}", response_model=Optional[OutTimeTracker])
async def get_time_tracker_by_id(
        service_time_tracker: TimeTrackerServiceDep,
        time_tracker_id: int,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
) -> Optional[
    OutTimeTracker]:
    await api_main_server.Access_token_accept(csat)
    return await service_time_tracker.get_time_tracker_by_id(time_tracker_id)


@router_time_tracker.get("/", response_model=Optional[OutTimeTracker])
async def get_time_tracker_by_task_id(
        service_time_tracker: TimeTrackerServiceDep,
        task_id: int,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
) -> Optional[
    OutTimeTracker]:
    await api_main_server.Access_token_accept(csat)
    return await service_time_tracker.get_time_tracker_by_task_id(task_id)


@router_time_tracker.post("/create", response_model=OutTimeTracker)
async def create_time_tracker(
        service_time_tracker: TimeTrackerServiceDep,
        data: CreateTimeTracker,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
) -> OutTimeTracker:
    await api_main_server.Access_token_accept(csat)
    return await service_time_tracker.create_time_tracker(data)


@router_time_tracker.patch("/update", response_model=Optional[OutTimeTracker])
async def update_time_tracker(
        service_time_tracker: TimeTrackerServiceDep,
        data: UpdateTimeTracker,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
) -> Optional[
    OutTimeTracker]:
    await api_main_server.Access_token_accept(csat)
    return await service_time_tracker.update_time_tracker(data)


@router_time_tracker.delete("/delete", response_model=Optional[OutTimeTracker])
async def delete_time_tracker(
        service_time_tracker: TimeTrackerServiceDep,
        time_tracker_id: int,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
) -> Optional[
    OutTimeTracker]:
    await api_main_server.Access_token_accept(csat)
    return await service_time_tracker.delete_time_tracker(time_tracker_id)
