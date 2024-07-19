from fastapi import HTTPException, UploadFile
from settings import urls
from httpx import AsyncClient, ReadTimeout


async def upload_file_logic(
    note_id: str, file: UploadFile, client: AsyncClient
) -> dict:
    url = f"{urls.file_service_url}/file/upload/{note_id}"
    files = {"file": (file.filename, file.file, file.content_type)}
    try:
        upl_file = await client.post(url, files=files)
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if upl_file.status_code == 200:
        return upl_file.json()
    else:
        raise HTTPException(status_code=404, detail=upl_file.json()["detail"])


async def delete_file_logic(note_id: str, file_name: str, client: AsyncClient) -> dict:
    url = f"{urls.file_service_url}/file/delete/{note_id}/filename/{file_name}"
    try:
        del_file = await client.delete(url)
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if del_file.status_code == 200:
        return del_file.json()
    else:
        raise HTTPException(status_code=404, detail=del_file.json()["detail"])


async def get_file_logic(note_id: str, file_name: str, client: AsyncClient) -> bytes:
    url = f"{urls.file_service_url}/file/{note_id}/{file_name}"
    try:
        response = await client.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if response.status_code == 200:
        return await response.aread()
    else:
        raise HTTPException(
            status_code=response.status_code, detail=response.json()["detail"]
        )


async def get_list_files_logic(note_id: str, client: AsyncClient) -> dict:
    url = f"{urls.file_service_url}/file/{note_id}"
    try:
        list_files = await client.get(url)
    except ReadTimeout:
        raise HTTPException(
            status_code=501, detail="Сервер не ответил за отведенное время."
        )
    if list_files.status_code == 200:
        return list_files.json()["list_files"]
    else:
        raise HTTPException(status_code=404, detail=list_files.json()["detail"])
