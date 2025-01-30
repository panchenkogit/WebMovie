from database.connect import Base

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
