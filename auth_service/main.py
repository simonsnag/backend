from fastapi import APIRouter, FastAPI
import uvicorn
from routers.users import user_router

app = FastAPI()

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8081)
