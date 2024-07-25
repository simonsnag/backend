from typing import Optional
from uuid import UUID
from bson import ObjectId
from fastapi import HTTPException
from db.mongo_db import mongodb
from models.note import Note
from pymongo.results import InsertOneResult

from schemas.note import DisplayNoteSchema


async def create_note_crud(note: Note) -> InsertOneResult:
    try:
        created_note = await mongodb.note_collection.insert_one(note.model_dump())
        return created_note
    except Exception:
        raise HTTPException(status_code=401, detail="Не удалось создать заметку")


async def get_note_crud(id: str) -> Optional[Note]:
    try:
        current_note = await mongodb.note_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(
            status_code=401, detail="Заметки не существует, отсутствует доступ."
        )
    if current_note is None:
        return None
    current_note["id"] = str(current_note["_id"])
    return Note.model_validate(current_note)


async def delete_note_crud(note: Note, id: str):
    try:
        note.is_delete = True
        result = await mongodb.basket_collection.insert_one(note.model_dump())
        await mongodb.note_collection.delete_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=401, detail="Не удалось удалить заметку.")
    return result


async def update_note_crud(id: str, data: dict) -> InsertOneResult:
    try:
        result = await mongodb.note_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Заметка не обновлена.")
    return result


async def get_all_notes_crud(user_id: UUID) -> list:
    try:
        notes = []
        async for note in mongodb.note_collection.find({"user_id": user_id}):
            note["id"] = str(note["_id"])
            notes.append(DisplayNoteSchema.model_validate(note))
    except Exception:
        raise HTTPException(status_code=401, detail="Не удалось получить заметки.")
    return notes


async def get_basket_crud(user_id: UUID) -> list:
    try:
        notes_in_basket = []
        async for note in mongodb.basket_collection.find({"user_id": user_id}):
            note["id"] = str(note["_id"])
            notes_in_basket.append(DisplayNoteSchema.model_validate(note))
    except Exception:
        raise HTTPException(
            status_code=401, detail="Не удалось получить заметки из корзины."
        )
    return notes_in_basket


async def restore_from_basket_crud(id: str, user_id: UUID) -> Note:
    try:
        current_note = await mongodb.basket_collection.find_one(
            {"_id": ObjectId(id), "user_id": user_id}
        )
        current_note["is_delete"] = False
        await mongodb.note_collection.insert_one(current_note)
        await mongodb.basket_collection.delete_one(
            {"_id": ObjectId(id), "user_id": user_id}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Не удалось восстановить заметку.")
    return Note.model_validate(current_note)


async def get_note_from_basket_crud(id: str) -> Optional[Note]:
    try:
        current_note = await mongodb.basket_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(
            status_code=401, detail="Заметки не существует, отсутствует доступ."
        )
    if current_note is None:
        return None
    return Note.model_validate(current_note)
