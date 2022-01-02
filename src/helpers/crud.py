from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models import models
from models.schemas import User, Item, UserCreate, ItemCreate
from .security import pwd_context


def get_user(db: Session, user_id: int) -> User:
    """
    Get user by user id

    :param db: Session
    :param user_id: int
    :return: User
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User:
    """
    Get user by username

    :param db: Session
    :param username: str
    :return: User
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> User:
    """
    Get all users via pagination

    :param db: Session
    :param skip: int
    :param limit: int
    :return: User
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create new user

    :param db: Session
    :param user: UserCreate
    :return: User
    """
    fake_hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, url: str) -> Item:
    """
    Get all items with url

    :param db: Session
    :param url: str
    :return: Item
    """
    item = ItemCreate(url=url)
    return get_or_create_item(db, item)


def check_item(db: Session, url: str) -> Item:
    """
    Check item is exist in last 10 mins
    :param db: Session
    :param url: str
    :return: Item
    """
    return (
        db.query(models.Item)
        .filter(
            models.Item.url == url,
            models.Item.created_at
            >= (datetime.now() - timedelta(minutes=10)).timestamp(),
        )
        .first()
    )


def get_or_create_item(db: Session, item: ItemCreate) -> Item:
    """
    Create item
    :param db: Session
    :param item: Item
    :return: Item
    """
    db_item = check_item(db, item.url)
    if db_item is None:
        from .manupulator import parse_rss

        res = parse_rss(item.url)

        db_item = models.Item(**item.dict())
        db_item.infos = res
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item
