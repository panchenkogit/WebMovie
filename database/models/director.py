from database.connect import Base

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from database.models.relationships import films_directors

class Director(Base):
    __tablename__ = 'directors'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    birthday = Column(Date, nullable=True)
    
    director_film = relationship("Film", secondary=films_directors, back_populates="film_director")