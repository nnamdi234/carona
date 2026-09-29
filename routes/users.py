from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserLogin
from controllers.users import create_user, login_user
from db import get_db

router = APIRouter(prefix="/users")

@router.post("/register", response_model=None)
async def create_account(user_input: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_input)

@router.post("/login")
async def login(login_input: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(db, login_input)