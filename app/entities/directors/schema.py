from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class DirectorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя режиссёра")
    birthday: Optional[date] = Field(None, description="Дата рождения режиссёра в формате YYYY-MM-DD")

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Имя режиссёра")
    birthday: Optional[date] = Field(None, description="Дата рождения режиссёра в формате YYYY-MM-DD"
    )

class Director(DirectorBase):
    id: int = Field(..., description="ID режиссёра")

    class Config:
        from_attributes = True
