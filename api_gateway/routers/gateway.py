import io
from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from httpx import AsyncClient
from client.client import get_async_client
from logic.file_logic import (
    delete_file_logic,
    get_file_logic,
    get_list_files_logic,
    upload_file_logic,
)
from logic.user_logic import (
    authentification_logic,
    get_user_logic,
    refreshing_access_logic,
    registration_logic,
)
from logic.note_logic import (
    create_note_logic,
    delete_note_logic,
    get_basket_logic,
    get_note_logic,
    get_notes_logic,
    restore_from_basket_logic,
    update_note_logic,
)
from routers.depends import get_token
from schemas.note import CreateNoteSchema, DisplayNoteSchema, UpdateNoteSchema
from schemas.user import UserAuthSchema, UserCreateSchema, UserDisplaySchema


bearer_scheme = HTTPBearer(bearerFormat="JWT")
gateway_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth", auto_error=False)


@gateway_router.post("/registration", response_model=UserDisplaySchema, tags=["User"])
async def registration(
    user: UserCreateSchema, client: AsyncClient = Depends(get_async_client)
) -> UserDisplaySchema:
    response = await registration_logic(user, client)
    return UserDisplaySchema.model_validate(response)


@gateway_router.post("/authentification", tags=["User"])
async def authentification(
    user: UserAuthSchema, client: AsyncClient = Depends(get_async_client)
):
    response = await authentification_logic(user, client)
    return response


@gateway_router.get("/refresh_access", tags=["User"])
async def refreshing_access(
    token: str = Depends(get_token), client: AsyncClient = Depends(get_async_client)
):
    refreshed_token = await refreshing_access_logic(token, client)
    return refreshed_token


@gateway_router.get("/note", tags=["Notes"])
async def get_notes(
    token: str = Depends(get_token), client: AsyncClient = Depends(get_async_client)
):
    user = await get_user_logic(token, client)
    notes = await get_notes_logic(user.id, client)
    return notes


@gateway_router.post("/note", response_model=DisplayNoteSchema, tags=["Notes"])
async def create_note(
    note: CreateNoteSchema,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    user = await get_user_logic(token, client)
    created_note = await create_note_logic(note, user.id, client)
    return DisplayNoteSchema.model_validate(created_note)


@gateway_router.get("/note/{note_id}", response_model=DisplayNoteSchema, tags=["Notes"])
async def get_note(
    note_id: str,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    user = await get_user_logic(token, client)
    current_note = await get_note_logic(note_id, user.id, client)
    return DisplayNoteSchema.model_validate(current_note)


@gateway_router.patch(
    "/note/{note_id}", response_model=DisplayNoteSchema, tags=["Notes"]
)
async def update_note(
    note_id: str,
    note_data: UpdateNoteSchema = Body(...),
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    user = await get_user_logic(token, client)
    current_note = await update_note_logic(note_id, note_data, user.id, client)
    return DisplayNoteSchema.model_validate(current_note)


@gateway_router.delete("/note/{note_id}", tags=["Notes"])
async def delete_note(
    note_id: str,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    user = await get_user_logic(token, client)
    current_note = await delete_note_logic(note_id, user.id, client)
    return current_note


@gateway_router.get("/basket", tags=["Basket"])
async def get_basket(
    token: str = Depends(get_token), client: AsyncClient = Depends(get_async_client)
):
    user = await get_user_logic(token, client)
    basket = await get_basket_logic(user.id, client)
    return basket


@gateway_router.get("/basket/{note_id}", tags=["Basket"])
async def restore_from_basket(
    note_id: str,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    user = await get_user_logic(token, client)
    restored_note = await restore_from_basket_logic(note_id, user.id, client)
    return DisplayNoteSchema.model_validate(restored_note)


@gateway_router.post("/note/{note_id}/file/upload", tags=["File"])
async def upload_file(
    note_id: str,
    file: UploadFile = File(...),
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    status_uploading = await upload_file_logic(note_id, file, client)
    return status_uploading


@gateway_router.delete("/note/{note_id}/file/{file_name}delete", tags=["File"])
async def delete_file(
    note_id: str,
    file_name: str,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    status_deleting = await delete_file_logic(note_id, file_name, client)
    return status_deleting


@gateway_router.get("/note/{note_id}/file/{file_name}", tags=["File"])
async def get_file(
    note_id: str,
    file_name: str,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    file = await get_file_logic(note_id, file_name, client)
    return StreamingResponse(
        io.BytesIO(file),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@gateway_router.get("/note/{note_id}/file", tags=["File"])
async def get_list_files(
    note_id: str,
    token: str = Depends(get_token),
    client: AsyncClient = Depends(get_async_client),
):
    list_files = await get_list_files_logic(note_id, client)
    return list_files
