from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate
from sqlalchemy import select
from models.users import User
from fastapi import HTTPException


async def create_user(db: AsyncSession, user_input: UserCreate):
    # check if email exists
    existing_email = await db.execute(
        select(User).where(User.email == user_input.email)
    )

    if existing_email.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )

    # check if phone_number exists if provided
    if user_input.phone_number:
        existing_phone_number = await db.execute(
            select(User).where(User.email == user_input.email)
        )

        if existing_phone_number.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=400,
                detail= "A user with this phonenumber already exists"
            )
