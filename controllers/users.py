from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserLogin
from sqlalchemy import select
from models.users import User
from fastapi import HTTPException
from utils.security import hash_password, verify_password


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
            select(User).where(User.phone_number == user_input.phone_number)
        )

        if existing_phone_number.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=400,
                detail= "A user with this phonenumber already exists"
            )

    new_user = User(
        first_name=user_input.first_name,
        last_name=user_input.last_name,
        email=user_input.email,
        phone_number=user_input.phone_number,
        password=hash_password(user_input.password),
        role="user"
    )


    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)

    return {"success": True, "message": "Account successfully created", "data": new_user}


async def login_user(db: AsyncSession, user_input: UserLogin):
    # Check if email exists
    result = await db.execute(
        select(User).where(User.email == user_input.email)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=403,
            detail="This account does not exist. Please register"
        )

    
    if not verify_password(user_input.password, user.password):
        raise HTTPException(
            status_code=403,
            detail="Incorrect password"
        )

    return {"success": True, "message": "logged in successfully", "data": None}