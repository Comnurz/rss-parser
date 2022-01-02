from typing import Dict, List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    url: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    url: str
    infos: List[Dict[str, str]]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(User):
    hashed_password: str
