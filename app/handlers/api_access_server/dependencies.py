from fastapi import Depends
from app.handlers.api_access_server.service import api_main_server
from app.handlers.api_access_server.interfaces import async_api_main_server


def get_api_main_service() -> async_api_main_server:
    # возвращаем конкретную реализацию, но тип аннотируем интерфейсом
    return api_main_server()


ApiMainServiceDep = Depends(get_api_main_service)
