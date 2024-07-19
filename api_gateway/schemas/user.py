import uuid
from pydantic import EmailStr
from schemas.base import BaseSchema


class UserDisplaySchema(BaseSchema):
    id: uuid.UUID
    email: EmailStr
    username: str


class UserCreateSchema(BaseSchema):
    username: str
    email: EmailStr
    password: str


class UserAuthSchema(BaseSchema):
    email: EmailStr
    password: str
