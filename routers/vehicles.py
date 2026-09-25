import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from controllers import vehicle_controller
from schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new vehicle",
    description="Create a vehicle record with plate number, make, model, colour, and capacity."
)
async def create_vehicle(
    vehicle_in: VehicleCreate,
    db: AsyncSession = Depends(get_db)
):
    """Route handler for vehicle creation. Delegates to vehicle_controller."""
    return await vehicle_controller.create_vehicle(db=db, vehicle_in=vehicle_in)


@router.get(
    "",
    response_model=List[VehicleResponse],
    status_code=status.HTTP_200_OK,
    summary="List vehicles",
    description="Retrieve a paginated list of active vehicles with optional filtering by owner_id."
)
async def list_vehicles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max number of records to return"),
    owner_id: Optional[uuid.UUID] = Query(None, description="Filter by vehicle owner ID"),
    db: AsyncSession = Depends(get_db)
):
    """Route handler for listing vehicles."""
    return await vehicle_controller.get_vehicles(
        db=db,
        skip=skip,
        limit=limit,
        owner_id=owner_id
    )


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get vehicle by ID",
    description="Retrieve details of a specific vehicle by its UUID."
)
async def get_vehicle(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Route handler for retrieving a single vehicle."""
    return await vehicle_controller.get_vehicle_by_id(db=db, vehicle_id=vehicle_id)


@router.patch(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a vehicle",
    description="Partially update vehicle attributes."
)
async def update_vehicle(
    vehicle_id: uuid.UUID,
    vehicle_in: VehicleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Route handler for updating vehicle details."""
    return await vehicle_controller.update_vehicle(
        db=db,
        vehicle_id=vehicle_id,
        vehicle_in=vehicle_in
    )


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a vehicle",
    description="Soft-delete a vehicle by its ID."
)
async def delete_vehicle(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Route handler for deleting a vehicle."""
    await vehicle_controller.delete_vehicle(db=db, vehicle_id=vehicle_id)
    return None
