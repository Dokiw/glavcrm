from typing import Protocol

from app.handlers.api_access_server.schemas import CheckSessionAccessToken


class async_api_main_server(Protocol):

    async def Access_token_accept(self, data: CheckSessionAccessToken):
        ...
