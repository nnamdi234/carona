from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.user import UserCreate, UserLogin
from utils.security import hash_password, verify_password


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Business logic for registering a new user."""
    # Check if email is already registered
    existing_user_email = await db.execute(
        select(User).where(User.email == user_in.email)
    )
    if existing_user_email.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    # Check if phone number is already registered (if provided)
    if user_in.phone_number:
        existing_user_phone = await db.execute(
            select(User).where(User.phone_number == user_in.phone_number)
        )
        if existing_user_phone.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this phone number already exists."
            )

    # Hash the password
    hashed_pwd = hash_password(user_in.password)

    # Create new user instance
    new_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        phone_number=user_in.phone_number,
        password=hashed_pwd,
        role=user_in.role
    )

    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)

    return new_user


async def authenticate_user(db: AsyncSession, credentials: UserLogin) -> User:
    """Business logic for verifying user login credentials."""
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Check for soft deletion
    if user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated."
        )

    # Verify password against hash
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    return user
