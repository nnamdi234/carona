from schemas.rides import RideCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from fastapi import APIRouter, Depends
from models import User
from utils.security import get_current_user
from controllers.rides import create_ride

router = APIRouter(prefix="/rides")

@router.post("/", response_model=None)
async def offer_ride(user_input: RideCreate,db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_ride(db, user_input, current_user)