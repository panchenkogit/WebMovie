from database.connect import Base

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    birthday = Column(Date, nullable=True)

    films = relationship("Film", secondary="film_director", back_populates="directors")
