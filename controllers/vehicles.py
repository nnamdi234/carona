import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from models.vehicles import Vehicle
from models.users import User
from schemas.vehicles import VehicleCreate


async def create_vehicle(db: AsyncSession, vehicle_input: VehicleCreate):
    # 1. Check if vehicle with plate_number already exists
    existing_plate = await db.execute(
        select(Vehicle).where(Vehicle.plate_number == vehicle_input.plate_number)
    )
    if existing_plate.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="A vehicle with this plate number already exists"
        )

    # 2. Check if owner_id exists if provided
    if vehicle_input.owner_id:
        owner = await db.execute(
            select(User).where(User.id == vehicle_input.owner_id)
        )
        if owner.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=404,
                detail="Owner user not found"
            )

    # 3. Create new vehicle
    new_vehicle = Vehicle(
        make=vehicle_input.make,
        model=vehicle_input.model,
        colour=vehicle_input.colour,
        capacity=vehicle_input.capacity,
        plate_number=vehicle_input.plate_number,
        owner_id=vehicle_input.owner_id
    )

    db.add(new_vehicle)
    await db.flush()
    await db.refresh(new_vehicle)

    return new_vehicle


async def get_vehicle(db: AsyncSession, vehicle_id: uuid.UUID):
    # Look up vehicle by ID
    result = await db.execute(
        select(Vehicle).where(Vehicle.id == vehicle_id)
    )
    vehicle = result.scalar_one_or_none()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


async def get_all_vehicles(db: AsyncSession):
    # Fetch all vehicles
    result = await db.execute(select(Vehicle))
    return result.scalars().all()
