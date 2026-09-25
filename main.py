from contextlib import asynccontextmanager
from fastapi import FastAPI

from db import engine
from models import Base
from routers import users_router, vehicles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-creates all tables on startup if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Carona API", 
    version="0.1.0",
    description="API for Carona carpooling service",
    summary="This API allows users to create and manage carpooling rides, view available rides, and join existing rides.",
    lifespan=lifespan
)

app.include_router(users_router)
app.include_router(vehicles_router)


@app.get("/health")
async def health():
    return {"status": "ok"}