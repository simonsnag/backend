import io
from minio import S3Error
from client.minio_cl import minio_client
from minio.error import S3Error
from fastapi import HTTPException, UploadFile


def _check_bucket(bucket_name: str):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        return True
    except Exception:
        return False


async def upload_file_logic(bucket_name: str, file: UploadFile) -> dict:
    check_bucket = _check_bucket(bucket_name)
    if not check_bucket:
        raise HTTPException(status_code=500, detail="Не удалось загрузить файлы")
    try:
        file_name = file.filename
        content_type = file.content_type
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=file.file,
            length=-1,
            part_size=16 * 1024 * 1024,
            content_type=content_type,
        )
        return {"message": "Файл загружен"}
    except S3Error:
        raise HTTPException(status_code=400, detail="Не удалось загрузить файл")


async def delete_file_logic(bucket_name: str, file_name: str) -> dict:
    try:
        minio_client.remove_object(bucket_name, file_name)
        return {"message": "Файл удален"}
    except S3Error:
        raise HTTPException(status_code=400, detail="Не удалось удалить файл")


async def get_file_logic(bucket_name: str, file_name: str) -> object:
    try:
        response = minio_client.get_object(
            bucket_name=bucket_name, object_name=file_name
        )
        file_data = io.BytesIO(response.read())
        return file_data
    except S3Error:
        raise HTTPException(status_code=400, detail="Не удалось загрузить файлы")


async def get_list_files_logic(bucket_name) -> list:
    try:
        list_files = []
        response = minio_client.list_objects(bucket_name=bucket_name, recursive=True)
        for object in response:
            list_files.append(object.object_name)
        return list_files
    except S3Error:
        raise HTTPException(status_code=400, detail="Не удалось загрузить файлы")
