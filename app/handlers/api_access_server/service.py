import logging
from typing import Optional

import aiohttp
import asyncio
from fastapi import HTTPException

from app.handlers.api_access_server.interfaces import async_api_main_server
from app.handlers.api_access_server.schemas import CheckSessionAccessToken


class api_main_server(async_api_main_server):

    async def Access_token_accept(self, data: CheckSessionAccessToken):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "http://localhost:9787/session/access_token",
                    json=data.dict()  # <-- конвертируем Pydantic модель в dict для JSON
            ) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    logging.info(f"Ошибка с запросом: {resp.status}, ответ: {text}")
                    raise HTTPException(
                        status_code=resp.status,
                        detail=f"Ошибка запроса к серверу: {text}"
                    )
                return await resp.json()

