from fastapi import HTTPException
from httpx import AsyncClient, ReadTimeout
from schemas.user import UserAuthSchema, UserCreateSchema, UserDisplaySchema
from settings import urls


async def registration_logic(user: UserCreateSchema, client: AsyncClient):
    url = f"{urls.auth_service_url}/user/create"
    try:
        response = await client.post(url, json=user.model_dump())
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail=response.json()["detail"])


async def authentification_logic(user: UserAuthSchema, client: AsyncClient):
    url = f"{urls.auth_service_url}/user/auth"
    try:
        response = await client.post(url, json=user.model_dump())
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail=response.json()["detail"])


async def get_user_logic(token: str, client: AsyncClient):
    get_user_url = f"{urls.auth_service_url}/user/auth"
    try:
        user = await client.get(get_user_url, headers={"token": token})
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if user.status_code == 200:
        return UserDisplaySchema.model_validate(user.json())
    else:
        raise HTTPException(status_code=404, detail=user.json()["detail"])


async def refreshing_access_logic(token: str, client: AsyncClient):
    refresh_token_url = f"{urls.auth_service_url}/user/refresh"
    try:
        refreshed_token = await client.get(refresh_token_url, headers={"token": token})
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if refreshed_token.status_code == 200:
        return refreshed_token.json()
    else:
        raise HTTPException(status_code=404, detail=refreshed_token.json()["detail"])
