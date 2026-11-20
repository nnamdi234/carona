from schemas.rides import RideCreate
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Vehicle
from sqlalchemy import select
from fastapi import HTTPException
from datetime import datetime, timezone
from models.ride import Ride


async def create_ride(db: AsyncSession, user_input:RideCreate, current_user:User):

    result = await db.execute(
        select(Vehicle).where(Vehicle.id == user_input.vehicle_id)
    )
    vehicle = result.scalar_one_or_none()

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    if vehicle.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only offer rides in your own vehicle"
        )

    if user_input.seats_offered > vehicle.capacity:
        raise HTTPException(
            status_code=400,
            detail="You can't offer more seats than your vehicle has"
        )

    if user_input.departure_time <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Departure time must be in the future"
        )
    
    new_ride = Ride(
        driver_id = current_user.id,
        vehicle_id = vehicle.id,
        origin = user_input.origin.strip(),
        destination = user_input.destination.strip(),
        departure_time = user_input.departure_time,
        seats_offered = user_input.seats_offered,
        fare = user_input.fare,
        status = "scheduled"
    )

    db.add(new_ride)
    await db.flush()
    await db.refresh(new_ride)

    return {"success": True, "message": "ride created successfully", "data": new_ride}