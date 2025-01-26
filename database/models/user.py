from database.connect import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.models.relationships import films_users


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    username = Column(String(12), index=True, unique=True)
    hash_password = Column(String)
    email = Column(String(30), index=True, unique=True)

    user_film = relationship("Film", secondary=films_users, back_populates="film_user")
    