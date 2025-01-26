from database.connect import Base

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    year = Column(Integer, index=True)
    rating = Column(Float)

    directors = relationship("Director", secondary="film_director", back_populates="films")
    liked_by_users = relationship("UserFilmLibrary", back_populates="film")



