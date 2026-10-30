from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database.connection import Settings
from routes.events import event_router
from routes.users import user_router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await settings.initialize_database()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)