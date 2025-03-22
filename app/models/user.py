from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String, nullable=True)  # Полное имя (опционально)
    age = Column(Integer, nullable=True)  # Возраст (опционально)
    weight = Column(Float, nullable=True)  # Вес (опционально)
    height = Column(Float, nullable=True)  # Рост (опционально)
    created_at = Column(DateTime, default=func.now())  # Дата регистрации
    is_active = Column(Boolean, default=True)  # Активен ли пользователь
    is_verified = Column(Boolean, default=False)  # Подтверждена ли почта
    verification_code = Column(String, nullable=True)  # Код подтверждения
    verification_code_expires_at = Column(DateTime, nullable=True)  # Срок действия кода

    refresh_token = Column(String, nullable=True)