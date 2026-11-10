import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
from routes.vehicles import router as vehicles_router
from contextlib import asynccontextmanager
from db import engine
from models import Base



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
    summary="This API allows users to create and manage carpooling rides, view available rides, and join existing rides.",
    lifespan=lifespan
)

# Browsers block a page from calling an API on another address (origin) unless
# the API says that address is allowed. The allowed frontends come from .env,
# comma-separated, e.g. CORS_ORIGINS=http://localhost:5173,https://carona.example
load_dotenv()
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],  # the frontend sends Content-Type and Authorization
)

app.include_router(user_router)
app.include_router(vehicles_router)


@app.get("/health")
async def health():
    return {"status": "ok"}