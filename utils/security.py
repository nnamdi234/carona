import bcrypt
from dotenv import load_dotenv
import jwt
from datetime import datetime, timezone, timedelta
import os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from db import get_db
from models.users import User

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password):
    salt =  bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')



def verify_password(plain, hashed):
    return bcrypt.checkpw(
        plain.encode("utf-8"),
        hashed.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired. Pleasse log in again"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token. Please log in again"
        )


security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await db.execute(
        select(User).where(User.id == UUID(user_id))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user