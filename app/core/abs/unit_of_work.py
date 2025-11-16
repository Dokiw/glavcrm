# app/core/abs/unit_of_work.py
from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from app.handlers.pipeline.interfaces import AsyncDepartmentRepository, AsyncPipelineRepository


class IUnitOfWorkDepart(AbstractAsyncContextManager, ABC):
    depart_repo: AsyncDepartmentRepository

    @property
    @abstractmethod
    def depart_repo(self) -> "AsyncDepartmentRepository":
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class IUnitOfWorkPipelineStage(AbstractAsyncContextManager, ABC):
    pipeline_repo: AsyncPipelineRepository

    @property
    @abstractmethod
    def pipeline_repo(self) -> "AsyncPipelineRepository":
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass