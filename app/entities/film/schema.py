from pydantic import BaseModel, Field, condecimal
from typing import Optional
from datetime import date


class FilmBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название фильма")
    description: str = Field(..., max_length=1000, description="Описание фильма")
    year: int = Field(..., ge=1900, le=date.today().year, description="Год выпуска фильма")
    rating: float = Field(..., ge=0, le=10, description="Рейтинг фильма (от 0 до 10)")

class FilmCreate(FilmBase):
    pass

class FilmUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Название фильма")
    description: Optional[str] = Field(None, max_length=1000, description="Описание фильма")
    year: Optional[int] = Field(None, ge=1900, le=date.today().year, description="Год выпуска фильма")
    rating: Optional[float] = Field(None, ge=0, le=10, description="Рейтинг фильма (от 0 до 10)")

class Film(FilmBase):
    id: int = Field(..., description="ID фильма")

    class Config:
        from_attributes = True
