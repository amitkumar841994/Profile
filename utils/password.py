from passlib.context import CryptContext

from fastapi import FastAPI,Depends,HTTPException,status
from jose import JWTError,jwt
from datetime import datetime,timedelta
from pydantic import BaseModel


# Secret keys and algorithms
SECRET_KEY = "vakjshdfaksjfh74356837lakjhdgflas457687sfgagask;jg"
REFRESH_SECRET_KEY = "b;lskdjftgq3849tuldsk;jgta654654awetfgaswzjnehtgf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# Helper functions
def create_token(data: dict, expires_delta: timedelta, secret_key: str):
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token(data: dict):
    """Create an access token."""
    return create_token(
        data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), SECRET_KEY
    )


def create_refresh_token(data: dict):
    """Create a refresh token."""
    return create_token(
        data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), REFRESH_SECRET_KEY
    )
 