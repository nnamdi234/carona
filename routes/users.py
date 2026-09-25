from fastapi import APIRouter, Depends
from models.users import User
from schemas.users import UserCreate
from controllers.users import create_user
from db import get_db

router = APIRouter(prefix="/users")

@router.post("/register", response_model=None)
async def create_account(user_input=UserCreate, db=Depends(get_db)):
    return await create_user(db, user_input)