from  pydantic import Field, BaseModel, EmailStr, NonNegativeInt

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=30, description="Имя пользователя от 2 до 30 символов")
    email: EmailStr = Field(..., min_length=6, max_length=30, description="Почта в формате @email")
    age: NonNegativeInt = Field(..., lt=101, description="Возраст от 1 до 101")

class UserRegister(UserBase):
    password: str = Field(..., min_length=4, max_length=20, description="Пароль от 4 до 20 символов")
    

class UserLogin(BaseModel):
    username: str = Field(..., min_length=2, max_length=30, description="Имя пользователя от 2 до 30 символов")
    password: str = Field(..., min_length=4, max_length=20, description="Пароль от 4 до 20 символов")


class User(UserBase):
    id: NonNegativeInt = Field(..., description="ID пользователя(автогенерация в БД)")
