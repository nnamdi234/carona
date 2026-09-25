import uuid
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.vehicles import Vehicle
from schemas.vehicle import VehicleCreate, VehicleUpdate


async def create_vehicle(
    db: AsyncSession,
    vehicle_in: VehicleCreate,
    current_user_id: Optional[uuid.UUID] = None
) -> Vehicle:
    """Create a new vehicle after checking for plate number uniqueness."""
    existing = await db.execute(
        select(Vehicle).where(
            Vehicle.plate_number == vehicle_in.plate_number,
            Vehicle.deleted_at.is_(None)
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A vehicle with this plate number already exists."
        )

    # Use explicitly passed owner_id or fallback to current_user_id
    owner_id = vehicle_in.owner_id or current_user_id

    new_vehicle = Vehicle(
        make=vehicle_in.make,
        model=vehicle_in.model,
        colour=vehicle_in.colour,
        capacity=vehicle_in.capacity,
        plate_number=vehicle_in.plate_number,
        owner_id=owner_id,
    )

    db.add(new_vehicle)
    await db.flush()
    await db.refresh(new_vehicle)
    return new_vehicle


async def get_vehicles(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    owner_id: Optional[uuid.UUID] = None
) -> List[Vehicle]:
    """Retrieve a list of active vehicles with optional filtering by owner."""
    query = select(Vehicle).where(Vehicle.deleted_at.is_(None))
    if owner_id is not None:
        query = query.where(Vehicle.owner_id == owner_id)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_vehicle_by_id(
    db: AsyncSession,
    vehicle_id: uuid.UUID
) -> Vehicle:
    """Retrieve a single active vehicle by its ID."""
    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id,
            Vehicle.deleted_at.is_(None)
        )
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found."
        )
    return vehicle


async def update_vehicle(
    db: AsyncSession,
    vehicle_id: uuid.UUID,
    vehicle_in: VehicleUpdate
) -> Vehicle:
    """Update fields on an existing vehicle."""
    vehicle = await get_vehicle_by_id(db=db, vehicle_id=vehicle_id)

    # If updating plate number, ensure new plate is not taken
    if vehicle_in.plate_number and vehicle_in.plate_number != vehicle.plate_number:
        plate_check = await db.execute(
            select(Vehicle).where(
                Vehicle.plate_number == vehicle_in.plate_number,
                Vehicle.id != vehicle_id,
                Vehicle.deleted_at.is_(None)
            )
        )
        if plate_check.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A vehicle with this plate number already exists."
            )

    update_data = vehicle_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vehicle, field, value)

    await db.flush()
    await db.refresh(vehicle)
    return vehicle


async def delete_vehicle(
    db: AsyncSession,
    vehicle_id: uuid.UUID
) -> None:
    """Soft-delete a vehicle by setting its deleted_at timestamp."""
    vehicle = await get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    vehicle.deleted_at = func.now()
    await db.flush()
