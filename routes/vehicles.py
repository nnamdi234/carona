from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.vehicles import VehicleCreate
from controllers.vehicles import create_vehicle, get_vehicle, get_all_vehicles
from db import get_db

router = APIRouter(prefix="/vehicles")


@router.post("", response_model=None)
async def add_vehicle(vehicle_input: VehicleCreate, db: AsyncSession = Depends(get_db)):
    return await create_vehicle(db, vehicle_input)


@router.get("", response_model=None)
async def list_vehicles(db: AsyncSession = Depends(get_db)):
    return await get_all_vehicles(db)


@router.get("/{vehicle_id}", response_model=None)
async def fetch_vehicle(vehicle_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_vehicle(db, vehicle_id)
