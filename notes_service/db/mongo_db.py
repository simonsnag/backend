from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from settings import mongo_settings


class MongoDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDB, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "client"):
            self.client = AsyncIOMotorClient(
                mongo_settings.database_url, uuidRepresentation="standard"
            )
            self.db = self.client[mongo_settings.mongo_name]
            self.note_collection = self.db.get_collection("note")
            self.basket_collection = self.db.get_collection("basket")

    async def setup_indexes(self):
        await self.note_collection.create_index([("user_id", pymongo.ASCENDING)])
        await self.basket_collection.create_index([("user_id", pymongo.ASCENDING)])


mongodb = MongoDB()
