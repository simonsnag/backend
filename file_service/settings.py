import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class MinioSettings(BaseSettings):
    access_key: str = os.environ.get("ACCESS_KEY")
    secret_key: str = os.environ.get("SECRET_KEY")
    minio_url: str = os.environ.get("MINIO_URL")
