from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    Базовая схема для пользователя.
    """
    username: str = Field(..., example="john_doe", description="Уникальное имя пользователя")
    email: EmailStr = Field(..., example="john.doe@example.com", description="Электронная почта пользователя")
    full_name: Optional[str] = Field(None, example="John Doe", description="Полное имя пользователя")
    age: Optional[int] = Field(None, example=25, description="Возраст пользователя")
    weight: Optional[float] = Field(None, example=70.5, description="Вес пользователя в кг")
    height: Optional[float] = Field(None, example=175.0, description="Рост пользователя в см")


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.
    """
    password: str = Field(..., example="strongpassword123", description="Пароль пользователя")


class UserUpdate(BaseModel):
    """
    Схема для обновления данных пользователя.
    """
    username: Optional[str] = Field(None, example="new_john_doe", description="Новое имя пользователя")
    email: Optional[EmailStr] = Field(None, example="new.john.doe@example.com", description="Новая электронная почта")
    full_name: Optional[str] = Field(None, example="New John Doe", description="Новое полное имя")
    age: Optional[int] = Field(None, example=26, description="Новый возраст пользователя")
    weight: Optional[float] = Field(None, example=71.0, description="Новый вес пользователя в кг")
    height: Optional[float] = Field(None, example=176.0, description="Новый рост пользователя в см")
    password: Optional[str] = Field(None, example="newstrongpassword123", description="Новый пароль")


class UserInDBBase(UserBase):
    """
    Базовая схема для пользователя, которая используется для возврата данных из базы данных.
    """
    id: int = Field(..., example=1, description="Уникальный идентификатор пользователя")
    is_active: bool = Field(..., example=True, description="Активен ли пользователь")
    is_verified: bool = Field(..., example=False, description="Подтверждена ли почта")
    created_at: datetime = Field(..., example="2023-10-01T12:00:00", description="Дата регистрации пользователя")

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """
    Схема для возврата данных о пользователе.
    """
    pass


class UserInDB(UserInDBBase):
    """
    Схема для внутреннего использования, например, для хранения данных в базе данных.
    """
    hashed_password: str = Field(..., example="hashedpassword123", description="Хэшированный пароль пользователя")
    verification_code: Optional[str] = Field(None, example="123456", description="Код подтверждения")
    verification_code_expires_at: Optional[datetime] = Field(None, example="2023-10-01T12:00:00", description="Срок действия кода")
    refresh_token: Optional[str] = Field(None, description="Refresh-токен пользователя")


class UserVerifyRequest(BaseModel):
    """
    Схема для запроса верификации почты.
    """
    email: EmailStr = Field(..., example="john.doe@example.com", description="Электронная почта для верификации")
    verification_code: str = Field(..., example="123456", description="Код подтверждения")
