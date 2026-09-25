from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from controllers import user_controller
from schemas.user import LoginResponse, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user by providing personal details and credentials."
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Route handler for user registration. Delegates business logic to user_controller."""
    return await user_controller.create_user(db=db, user_in=user_in)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user by email and password."
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Route handler for user login. Delegates verification and token issuance to user_controller."""
    return await user_controller.authenticate_user(db=db, credentials=credentials)


