from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import app.crud.auth as crud
import app.models.auth as models
from app.database import SessionLocal, engine
from app.schemas.auth import Token, TokenData, User, UserAuth
from app.utils.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    verify_password,
)

auth_router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    # do msal authentication with username and password here:
    user = crud.get_user_by_username(db, username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@auth_router.get("/me", response_model=User)
async def get_me_user(current_user: User = Depends(get_current_active_user)):
    """
    Get current user.

    Parameters
    ----------
    current_user : User
        Current user.

    Returns
    -------
    User
        Current user.

    Raises
    ------
    HTTPException
        If user is inactive.
    """
    return current_user


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Generate access token for user.
    If user is not present in app databasse, create user.

    Parameters
    ----------
    form_data : OAuth2PasswordRequestForm
        Form data for user login.
    db : Session
        Database session.

    Returns
    -------
    dict
        Access token and token type.

    Raises
    ------
    HTTPException
        If user credentials are incorrect.
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/create", response_model=User)
def create_user(user: UserAuth, db: Session = Depends(get_db)):
    """
    Create new user.

    Parameters
    ----------
    user : UserAuth
        User data.
    db : Session
        Database session.

    Returns
    -------
    User
        New user.

    Raises
    ------
    HTTPException
        If username or email is already registered.
    """
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = crud.get_user_by_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db=db, user=user)

    return user
