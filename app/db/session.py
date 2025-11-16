# app/db/session.py
from typing import AsyncGenerator, Annotated
import redis.asyncio as redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

DATABASE_URL = (
    f"{settings.DB_TYPE}+{settings.DB_ENGINE}://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # часто удобно отключить
)


# dependency для FastAPI — возвращает AsyncSession через async context manager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        # session автоматически закроется и await'ится при выходе


# # Инициализация клиента
# redis_client = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=0,
#     decode_responses=True  # если хочешь получать строки вместо байтов
# )
#
#
# async def get_redis() -> AsyncGenerator[redis.Redis, None]:
#     try:
#         yield redis_client
#     finally:
#         # Важно: не закрывай клиент после каждого запроса!
#         # Иначе потеряешь соединения
#         pass
#
#
# RedisDep = Annotated[redis.Redis, Depends(get_redis)]
