from sqlalchemy import Column, Float, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.connect import Base


class UserFilmLibrary(Base):
    __tablename__ = "user_film_library"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), primary_key=True)
    user_rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="liked_films")
    film = relationship("Film", back_populates="liked_by_users")

class FilmDirector(Base):
    __tablename__ = "film_director"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id", ondelete="CASCADE"), nullable=False)


class FilmGenre(Base):
    __tablename__ = "film_genre"

    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)


class FilmGenre(Base):
    __tablename__ = "film_genre"

    film_id = Column(Integer, ForeignKey("films.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)


