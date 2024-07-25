import logging
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class MongoSettings(BaseSettings):
    @property
    def database_url(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/?authSource=admin"

    mongo_host: str = os.environ.get("mongo_host")
    mongo_port: str = os.environ.get("mongo_port")
    mongo_name: str = os.environ.get("mongo_name")
    mongo_user: str = os.environ.get("mongo_user")
    mongo_password: str = os.environ.get("mongo_password")


mongo_settings = MongoSettings()


class ESSettings(BaseSettings):
    es_host: str = os.environ.get("es_host")
    es_port: int = os.environ.get("es_port")


es_settings = ESSettings()


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
