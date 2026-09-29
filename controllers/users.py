from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserLogin
from sqlalchemy import select
from models.users import User
from fastapi import HTTPException
from utils.security import create_access_token, verify_password, hash_password


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

    return new_user


async def login_user(db: AsyncSession, login_input: UserLogin):
    # 1. Look up user by email
    result = await db.execute(
        select(User).where(User.email == login_input.email)
    )
    user = result.scalar_one_or_none()

    # 2. Check if user exists
    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found"
        )

    # 3. Check if password is correct
    if not verify_password(login_input.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    # 4. Create simple JWT access token
    token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
