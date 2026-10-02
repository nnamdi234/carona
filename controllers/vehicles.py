from sqlalchemy.ext.asyncio import AsyncSession
from schemas.vehicles import VehicleCreate
from sqlalchemy import select
from models.vehicles import Vehicle
from fastapi import HTTPException


async def create_vehicle(db: AsyncSession, user_input: VehicleCreate):
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
        plate_number = user_input.plate_number
    )

    db.add(new_vehicle)
    await db.flush()
    await db.refresh(new_vehicle)

    return {"success": True, "message": "vehicle created successfully", "data": new_vehicle}