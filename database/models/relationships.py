from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.connect import Base


class UserFilmLibrary(Base):
    __tablename__ = "user_film_library"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="liked_films")
    film = relationship("Film", back_populates="liked_by_users")


class FilmDirector(Base):
    __tablename__ = "film_director"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id", ondelete="CASCADE"), nullable=False)


