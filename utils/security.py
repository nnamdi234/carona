import bcrypt
from dotenv import load_dotenv
import jwt
from datetime import datetime, timezone, timedelta
import os

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


