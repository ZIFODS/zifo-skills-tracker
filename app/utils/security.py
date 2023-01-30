from datetime import datetime, timedelta

from decouple import config
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = config(
    "API_SECRET_KEY"
)  # to get a string like this run: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token that expires in 15 minutes

    Parameters
    ----------
    data : dict
        The data to be encoded in the token
    expires_delta : timedelta, optional
        The time delta for the token to expire, by default None

    Returns
    -------
    str
        The encoded token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
