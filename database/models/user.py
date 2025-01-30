from database.connect import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.models.relationships import UserFilmLibrary



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    username = Column(String(50), index=True, unique=True)
    hash_password = Column(String, nullable=False)
    email = Column(String(50), index=True, unique=True)

    liked_films = relationship("UserFilmLibrary", back_populates="user")