import json
from typing import Optional

from app.db.session import RedisDep
from app.handlers.redis_cli.interfaces import AsyncRedisRepository


class RedisRepository(AsyncRedisRepository):

    def __init__(self, redis: RedisDep):
        self.redis = redis

    async def set_value(self, key: str, data: dict, ttl: int | None = None) -> Optional[bool]:
        value = json.dumps(data)
        return await self.redis.set(key, value, ex=ttl)

    async def get_value(self, key: str) -> Optional[dict]:
        raw = await self.redis.get(key)
        return json.loads(raw) if raw else None

    async def delete_value(self, key: str) -> Optional[bool]:
        return await self.redis.delete(key)









