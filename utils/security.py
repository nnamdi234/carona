import os
import jwt
import bcrypt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict) -> str:
    """Create a simple signed JWT access token."""
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
