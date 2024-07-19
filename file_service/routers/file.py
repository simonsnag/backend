from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from logic.file import (
    delete_file_logic,
    get_file_logic,
    get_list_files_logic,
    upload_file_logic,
)

file_router = APIRouter()


@file_router.post("/upload/{bucket_name}")
async def upload_file_to_note(bucket_name: str, file: UploadFile):
    result = await upload_file_logic(bucket_name, file)
    return result


@file_router.delete("/delete/{bucket_name}/filename/{filename}")
async def delete_note_bucket(bucket_name: str, filename: str):
    result = await delete_file_logic(bucket_name, filename)
    return result


@file_router.get("/{bucket_name}/{file_name}")
async def get_file(bucket_name: str, file_name: str):
    file = await get_file_logic(bucket_name, file_name)
    return StreamingResponse(
        file,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@file_router.get("/{bucket_name}")
async def get_list_files(bucket_name: str):
    list_files = await get_list_files_logic(bucket_name)
    return {"list_files": list_files}
