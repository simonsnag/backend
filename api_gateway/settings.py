from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class URLSettings(BaseSettings):
    auth_service_url: str
    notes_service_url: str
    file_service_url: str


urls = URLSettings()
