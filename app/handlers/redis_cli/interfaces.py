from typing import Protocol, Optional


class AsyncRedisRepository(Protocol):

    async def set_value(self, key: str, data: dict, ttl: int | None = None) -> Optional[bool]:
        ...

    async def get_value(self, key: str) -> Optional[dict]:
        ...

    async def delete_value(self, key: str) -> Optional[bool]:
        ...








