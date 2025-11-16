from typing import Optional

from app.handlers.api_glavrekl.schemas import LogInUser, AuthResponse
from app.handlers.api_glavrekl.interfaces import AsyncApiMainServer


# from app.method.initdatatelegram import verify_telegram_init_data

class ApiMainServer(AsyncApiMainServer):

    def __init__(self,access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    async def auth_by_login(self, login_data: LogInUser) -> Optional[AuthResponse]:
        return None

    async def auth_by_telegram(self, client_id: str, user_data) -> Optional[AuthResponse]:
        return None

    async def get_role(self,access_token):
        return None

    async def create_payment(self):
        return None

    async def create_or_get_wallet(self):
        return None

    async def get_by_user_id(self):
        return None

    async def refresh_session(self,refresh_token):
        return None

