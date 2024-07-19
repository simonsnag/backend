from minio import Minio

from settings import MinioSettings


minio_settings = MinioSettings()
minio_client = Minio(
    minio_settings.minio_url.replace("http://", "").replace("https://", ""),
    access_key=minio_settings.access_key,
    secret_key=minio_settings.secret_key,
    secure=False,
)
