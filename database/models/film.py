from database.connect import Base

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from database.models.relationships import films_directors, films_users

class Film(Base):
    __tablename__ = 'films'

    id =  Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    year =  Column(Integer, index=True)
    rating =  Column(Float)

    film_director = relationship("Director", secondary=films_directors, back_populates='director_film')
    film_user = relationship("User", secondary=films_users, back_populates='user_film')
    



