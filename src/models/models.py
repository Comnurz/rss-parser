import uuid as uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, JSON, Float


from utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    created_at = Column(Float, default=datetime.now().timestamp())
    infos = Column(JSON, nullable=False)

    def dict(self):
        return {"info": self.infos, "url": self.url}
