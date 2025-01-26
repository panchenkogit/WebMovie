from database.connect import Base

from sqlalchemy import Column, Table, ForeignKey


films_directors = Table(
    "film_director",
    Base.metadata,
    Column('film_id', ForeignKey('films.id', ondelete="CASCADE"), primary_key=True, index=True),
    Column('director_id', ForeignKey('directors.id', ondelete="CASCADE"), primary_key=True, index=True),
)

films_users = Table(
    "user_film_library",
    Base.metadata,
    Column('users_id', ForeignKey('users.id', ondelete="CASCADE"), primary_key=True, index=True),
    Column('films_id', ForeignKey('films.id', ondelete="CASCADE"), primary_key=True, index=True),
)
