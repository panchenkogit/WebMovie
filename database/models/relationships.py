from database.connect import Base

from sqlalchemy import Column, Table, ForeignKey


films_directors = Table(
    "film_director",
    Base.metadata,
    Column('film_id', ForeignKey('films.id', ondelete="CASCADE"), primary_key=True, index=True),
    Column('director_id', ForeignKey('directors.id', ondelete="CASCADE"), primary_key=True, index=True),
)
