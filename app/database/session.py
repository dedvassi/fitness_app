import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Берем строку подключения к базе из .env, если нет — используем SQLite по умолчанию
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitness_app.db")

# Создаем движок базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Создаем сессию для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определяем базовую модель для ORM
Base = declarative_base()

# Функция для получения сессии БД (для зависимостей в FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
