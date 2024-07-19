from datetime import datetime
from typing import Annotated
from pydantic import BeforeValidator
from schemas.base import BaseSchema


PyObjectId = Annotated[str, BeforeValidator(str)]


class CreateNoteSchema(BaseSchema):
    title: str
    content: str


class DisplayNoteSchema(BaseSchema):
    title: str
    content: str
    time_updated: datetime


class GetNoteSchema(BaseSchema):
    id: PyObjectId


class UpdateNoteSchema(BaseSchema):
    title: str
    content: str
