# app/core/abs/unit_of_work.py
from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TypeVar, Generic

from app.handlers.lead.interfaces import AsyncMasterLeadRepository, AsyncSubLeadRepository
from app.handlers.pipeline.interfaces import AsyncDepartmentRepository, AsyncPipelineRepository

TRepo = TypeVar("TRepo")


class IUnitOfWork(AbstractAsyncContextManager, Generic[TRepo], ABC):
    repo: TRepo

    @property
    @abstractmethod
    def repo(self) -> TRepo:
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
