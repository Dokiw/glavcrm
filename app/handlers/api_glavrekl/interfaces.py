from typing import Protocol, Optional

class AsyncApiMainServer(Protocol):

    # Возможно не надо из-за спец.
    # async def auth_by_login(self, login_data: LogInUser) -> Optional[AuthResponse]:
    #     ...
    #
    # async def auth_by_telegram(self, client_id: str, user_data: ProviderLoginRequest) -> Optional[AuthResponse]:
    #     ...

    async def get_role(self, access_token: str):
        ...

    async def create_payment(self):
        ...

    async def create_or_get_wallet(self):
        ...

    async def get_by_user_id(self):
        ...

    async def refresh_session(self,refresh_token: str):
        ...



