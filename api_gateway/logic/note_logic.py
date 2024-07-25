from uuid import UUID
from fastapi import HTTPException
from httpx import AsyncClient, ReadTimeout

from schemas.note import CreateNoteSchema, UpdateNoteSchema
from settings import urls


async def get_notes_logic(user_id: UUID, client: AsyncClient):
    get_notes_url = f"{urls.notes_service_url}/note"
    try:
        get_notes = await client.get(get_notes_url, headers={"user-data": str(user_id)})
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if get_notes.status_code == 200:
        return get_notes.json()
    else:
        raise HTTPException(status_code=404, detail=get_notes.json()["detail"])


async def create_note_logic(note: CreateNoteSchema, user_id: UUID, client: AsyncClient):
    create_note_url = f"{urls.notes_service_url}/note/create"
    try:
        create_note = await client.post(
            create_note_url,
            json=note.model_dump(),
            headers={"user-data": str(user_id)},
        )
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if create_note.status_code == 200:
        return create_note.json()
    else:
        raise HTTPException(status_code=404, detail=create_note.json()["detail"])


async def get_note_logic(note_id: str, user_id: UUID, client: AsyncClient):
    get_note_url = f"{urls.notes_service_url}/note/{note_id}"
    try:
        getting_note = await client.get(
            get_note_url, headers={"user-data": str(user_id)}
        )
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if getting_note.status_code == 200:
        return getting_note.json()
    else:
        raise HTTPException(status_code=404, detail=getting_note.json()["detail"])


async def update_note_logic(
    note_id: str, note_data: UpdateNoteSchema, user_id: UUID, client: AsyncClient
):
    update_note_url = f"{urls.notes_service_url}/note/{note_id}"
    try:
        updated_note = await client.patch(
            update_note_url,
            json=note_data.model_dump(),
            headers={"user-data": str(user_id)},
        )
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if updated_note.status_code == 200:
        return updated_note.json()
    else:
        raise HTTPException(status_code=404, detail=updated_note.json()["detail"])


async def delete_note_logic(note_id: str, user_id: UUID, client: AsyncClient):
    delete_note_url = f"{urls.notes_service_url}/note/{note_id}"
    try:
        updated_note = await client.delete(
            delete_note_url,
            headers={"user-data": str(user_id)},
        )
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if updated_note.status_code == 200:
        return updated_note.json()
    else:
        raise HTTPException(status_code=404, detail=updated_note.json()["detail"])


async def get_basket_logic(user_id: UUID, client: AsyncClient):
    get_basket_url = f"{urls.notes_service_url}/basket"
    try:
        basket = await client.get(get_basket_url, headers={"user-data": str(user_id)})
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if basket.status_code == 200:
        return basket.json()
    else:
        raise HTTPException(status_code=404, detail=basket.json()["detail"])


async def restore_from_basket_logic(note_id: str, user_id: UUID, client: AsyncClient):
    restore_from_basket_url = f"{urls.notes_service_url}/basket/{note_id}"
    try:
        restored_note = await client.get(
            restore_from_basket_url, headers={"user-data": str(user_id)}
        )

    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if restored_note.status_code == 200:
        return restored_note.json()
    else:
        raise HTTPException(status_code=404, detail=restored_note.json()["detail"])


async def search_note_logic(query: str, user_id: UUID, client: AsyncClient):
    search_url = f"{urls.notes_service_url}/search"
    try:
        found_notes = await client.get(
            search_url, headers={"user-data": str(user_id)}, params={"query": query}
        )
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if found_notes.status_code == 200:
        return found_notes.json()
    else:
        raise HTTPException(status_code=404, detail=found_notes.json()["detail"])
