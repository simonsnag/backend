from fastapi import FastAPI
import uvicorn
from routers.file import file_router

app = FastAPI()

app.include_router(file_router, prefix="/file", tags=["File"])


if __name__ == "__main__":
    uvicorn.run(app, port=8003)
