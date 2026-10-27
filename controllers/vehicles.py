from sqlalchemy.ext.asyncio import AsyncSession
from schemas.vehicles import VehicleCreate
from sqlalchemy import select
from models import Vehicle
from fastapi import HTTPException
from uuid import UUID
from models import User

async def create(db: AsyncSession, user_input: VehicleCreate, current_user: User):
    # check if plate number already exists
    existing_vehicle = await db.execute(
        select(Vehicle).where(Vehicle.plate_number == user_input.plate_number)
    )

    if existing_vehicle.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already exists"
        )

    new_vehicle = Vehicle(
        make = user_input.make,
        model = user_input.model,
        colour = user_input.colour,
        capacity = user_input.capacity,
        plate_number = user_input.plate_number,
        owner_id = current_user.id
    )

    db.add(new_vehicle)
    await db.flush()
    await db.refresh(new_vehicle)

    return {"success": True, "message": "vehicle created successfully", "data": new_vehicle}

async def get_all_vehicles(db:AsyncSession):
    result = await db.execute(
        select(Vehicle)
    )

    vehicles = result.scalars().all()

    return {"success": True, "message": "vehicles retrieved successfully", "data": vehicles}

async def get_vehicle_by_id(db: AsyncSession, vehicle_id: UUID):

    result = await db.execute(
        select(Vehicle).where(Vehicle.id == vehicle_id)
    )

    vehicle = result.scalar_one_or_none()

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return {"success": True, "message": "vehicle retrieved successfully", "data": vehicle}