from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.vehicles import VehicleCreate
from db import get_db
from controllers.vehicles import create, get_all_vehicles, get_vehicle_by_id
from uuid import UUID
 

router = APIRouter(prefix="/vehicles")

@router.post("/", response_model=None)
async def create_vehicle(user_input: VehicleCreate, db: AsyncSession = Depends(get_db)):
    return await create(db, user_input)

@router.get("/", response_model=None)
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_vehicles(db)


@router.get("/{vehicle_id}", response_model=None)
async def get(vehicle_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_vehicle_by_id(db, vehicle_id)