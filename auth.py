from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("DEADLINE"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "ini": int(datetime.now(timezone.utc).timestamp()),
            "exp": int(expire.timestamp()),
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), expire


def decode_access_token(token: str):
    # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # print("Get token", payload)
    # return payload
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Get token", payload)
        return payload
    except JWTError:
        print(JWTError)
        return None
