from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate
from controllers.users import create_user
from db import get_db
from schemas.users import UserLogin
from controllers.users import login_user
from controllers.users import get_all_users

router = APIRouter(prefix="/users")

@router.post("/register", response_model=None)
async def create_account(user_input: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_input)


@router.post("/login", response_model=None)
async def login_account(user_input:UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(db, user_input)


@router.get("/", response_model=None)
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)