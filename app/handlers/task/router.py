from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends

from app.handlers.api_access_server.dependencies import ApiMainServiceDep
from app.handlers.api_access_server.interfaces import async_api_main_server
from app.handlers.api_access_server.schemas import CheckSessionAccessToken
from app.handlers.task.dependencies import TaskServiceDep
from app.handlers.task.schemas import OutTask, CreateTask, UpdateTask
from app.method.get_token import get_token

router_Task = APIRouter(prefix="/Task", tags=["Task"])


@router_Task.get("/")
async def hub():
    return HTTPException(200, 'Status - True')


@router_Task.get("/{task_id}", response_model=Optional[OutTask])
async def get_task_by_id(
        service_task: TaskServiceDep,
        task_id: int,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
):
    await api_main_server.Access_token_accept(csat)
    return await service_task.get_task_by_id(task_id)


@router_Task.get("/sublead", response_model=Optional[List[OutTask]])
async def get_task_by_sub_lead_id(
        service_task: TaskServiceDep,
        sub_lead_id: int,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
):
    await api_main_server.Access_token_accept(csat)
    return await service_task.get_task_by_sub_lead_id(sub_lead_id)


@router_Task.post("/create", response_model=OutTask)
async def create_task(
        service_task: TaskServiceDep,
        data: CreateTask,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
):
    await api_main_server.Access_token_accept(csat)
    return await service_task.create_task(data)


@router_Task.patch("/update", response_model=Optional[OutTask])
async def update_task(
        service_task: TaskServiceDep,
        data: UpdateTask,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
):
    await api_main_server.Access_token_accept(csat)
    return await service_task.update_task(data)


@router_Task.delete("/delete", response_model=OutTask)
async def delete_task_by_id(
        service_task: TaskServiceDep,
        task_id: int,
        api_main_server: async_api_main_server = ApiMainServiceDep,
        csat: CheckSessionAccessToken = Depends(get_token),
):
    await api_main_server.Access_token_accept(csat)
    return await service_task.delete_task_by_id(task_id)
