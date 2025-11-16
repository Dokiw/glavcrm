from typing import Optional

from fastapi import APIRouter, HTTPException

from app.handlers.pipeline.dependencies import DepartServiceDep, PipelineServiceDep
from app.handlers.pipeline.schemas import output_department, create_department, update_department, \
    output_pipeline_stage, settings_pipeline_stage, create_pipeline_stage, update_pipeline_stage

router_Depart = APIRouter(prefix="/Depart", tags=["Depart"])


@router_Depart.get("/")
async def hub():
    return HTTPException(200, 'Status - True')


@router_Depart.get("/{depart_id}", response_model=Optional[output_department])
async def get_department_by_id(
        service_depart: DepartServiceDep,
        depart_id: int
):
    return await service_depart.get_department_by_id(depart_id)


@router_Depart.post("/create", response_model=output_department)
async def create_department(
        service_depart: DepartServiceDep,
        depart_data: create_department
):
    return await service_depart.create_department(depart_data)


@router_Depart.post("/update", response_model=Optional[output_department])
async def update_department(
        service_depart: DepartServiceDep,
        depart_data: update_department
):
    return await service_depart.update_department(depart_data)


@router_Depart.delete("/delete/{depart_id}", response_model=Optional[output_department])
async def delete_department_by_id(
        service_depart: DepartServiceDep,
        depart_id: int
):
    return await service_depart.delete_department_by_id(depart_id)


# ---------------------- pipeline -----------------------

router_Pipeline = APIRouter(prefix="/Pipeline", tags=["Pipeline"])


@router_Pipeline.get("/{pipeline_id}", response_model=Optional[output_pipeline_stage])
async def get_pipeline_stage_by_id(
        service_pipeline: PipelineServiceDep,
        pipeline_id: int
):
    return await service_pipeline.get_pipeline_stage_by_id(pipeline_id)


@router_Pipeline.post("/create", response_model=output_pipeline_stage)
async def create_pipeline_stage(
        service_pipeline: PipelineServiceDep,
        pipeline_data: create_pipeline_stage,
        settings: settings_pipeline_stage
):
    return await service_pipeline.create_pipeline_stage(pipeline_data, settings)


@router_Pipeline.post("/update", response_model=output_pipeline_stage)
async def update_pipeline_stage(
        service_pipeline: PipelineServiceDep,
        pipeline_data: update_pipeline_stage,
        settings: settings_pipeline_stage
):
    return await service_pipeline.update_pipeline_stage(pipeline_data, settings)


@router_Pipeline.delete("/delete/{pipeline_id}",response_model=Optional[output_pipeline_stage])
async def delete_pipeline_stage_by_id(
    service_pipeline: PipelineServiceDep,
    pipeline_id: int
):
    return await service_pipeline.delete_pipeline_stage_by_id(pipeline_id)