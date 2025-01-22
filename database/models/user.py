from database.connect import Base

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(12), index=True, unique=True)
    hash_password = Column(String)
    email = Column(String(30), index=True, unique=True)
    