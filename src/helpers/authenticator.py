from datetime import datetime
from typing import Optional, Dict

import jwt
from fastapi import Depends, HTTPException, status
from pydantic.schema import timedelta
from sqlalchemy.orm import Session

from helpers import crud
from helpers.security import pwd_context, SECRET_KEY, ALGORITHM, oauth2_scheme
from models.schemas import TokenData, User
from jose import JWTError
from utils.database import get_db


def authenticate_user(email: str, password: str, db: Session):
    """
    Authenticate user with email and password

    :param email: str
    :param password: str
    :param db: Session
    :return: User or False
    """
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify user password

    :param plain_password: str
    :param hashed_password: str
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    get hashed password
    :param password: str
    :return: str
    """
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, str], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generate JWT token
    :param data: Dict[str, str]
    :param expires_delta: Optional[timedelta]
    :return: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Get current user
    :param token: str
    :param db: Session
    :return: User
    """
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
        TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get active user

    :param current_user: User
    :return: User
    """
    return current_user
