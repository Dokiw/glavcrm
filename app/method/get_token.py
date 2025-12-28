from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.models import APIKey

from app.handlers.api_access_server.schemas import CheckSessionAccessToken

bearer_scheme = HTTPBearer(auto_error=False)  # auto_error=False чтобы можно было вручную бросать 401


async def get_token(user_id: int, request: Request = None, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> CheckSessionAccessToken:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = credentials.credentials

    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # Здесь можно добавить проверку JWT или любую асинхронную проверку токена
    # await some_async_verification(token)
    data = CheckSessionAccessToken(
        user_id=user_id,
        access_token=token,
        ip_address=ip,
        user_agent=user_agent,
    )
    return data
