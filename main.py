from fastapi import FastAPI     
from routes.users import router as user_router
from contextlib import asynccontextmanager
from db import engine
from models.base import Base



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Perform any cleanup tasks here

app = FastAPI(
    title="Carona API", 
    version= "0.1.0",
    description="API for Carona carpooling service",
    summary="This API allows users to create and manage carpooling rides, view available rides, and join existing rides."
)

app.include_router(user_router)

@app.get("/health")
async def health():
    return {"status": "ok"}