from fastapi import APIRouter, FastAPI
import uvicorn
import logging
from routers.note import note_router, basket_router, search_router
from db.mongo_db import mongodb

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(note_router, prefix="/note", tags=["note"])
main_api_router.include_router(basket_router, prefix="/basket", tags=["basket"])
main_api_router.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(main_api_router)


@app.on_event("startup")
async def on_startup():
    await mongodb.setup_indexes()


if __name__ == "__main__":
    uvicorn.run(app, port=8002)
