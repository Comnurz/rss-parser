from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from helpers import crud
from models import schemas
from utils.database import get_db

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create new user

    :param user: UserCreate
    :param db: Session
    :return: User
    """
    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users

    :param skip: int
    :param limit: int
    :param db: Session
    :return: List[User]
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
