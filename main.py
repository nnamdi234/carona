from fastapi import FastAPI
from routers import users_router, vehicles_router

app = FastAPI(
    title="Carona API", 
    version="0.1.0",
    description="API for Carona carpooling service",
    summary="This API allows users to create and manage carpooling rides, view available rides, and join existing rides."
)

app.include_router(users_router)
app.include_router(vehicles_router)


@app.get("/health")
async def health():
    return {"status": "ok"}