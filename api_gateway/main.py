from fastapi import FastAPI
import uvicorn
from routers.gateway import gateway_router

app = FastAPI()
app.include_router(gateway_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=True)
