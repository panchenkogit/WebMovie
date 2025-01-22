from pydantic import Field, BaseModel, EmailStr, NonNegativeInt, model_validator
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=30, description="Имя пользователя от 2 до 30 символов")
    email: EmailStr = Field(..., min_length=6, max_length=30, description="Почта в формате @email")
    age: NonNegativeInt = Field(..., lt=101, description="Возраст от 1 до 100")

class UserRegister(UserBase):
    password: str = Field(..., min_length=4, max_length=20, description="Пароль от 4 до 20 символов")

class UserLogin(BaseModel):
    username: str = Field(..., min_length=2, max_length=30, description="Имя пользователя от 2 до 30 символов")
    password: str = Field(..., min_length=4, max_length=20, description="Пароль от 4 до 20 символов")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=30, description="Имя пользователя от 2 до 30 символов")
    email: Optional[EmailStr] = Field(None, min_length=6, max_length=30, description="Почта в формате @email")
    age: Optional[NonNegativeInt] = Field(None, lt=101, description="Возраст от 1 до 100")
    password: Optional[str] = Field(None, min_length=4, max_length=20, description="Пароль от 4 до 20 символов")

    @model_validator(mode='before')
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class User(UserBase):
    id: NonNegativeInt = Field(..., description="ID пользователя (автогенерация в БД)")

    class Config:
        from_attributes = True
