from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from helpers import crud
from models import schemas
from utils.database import get_db

router = APIRouter()


@router.get("/item/", response_model=schemas.Item)
def read_items(url: str, db: Session = Depends(get_db)):
    """
    Get rss item

    :param url: str
    :param db: Session
    :return: List[Item]
    """
    items = crud.get_items(db, url=url)
    return items
