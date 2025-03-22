from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request, Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.token import TokenSchema, TokenRefreshRequest
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция для хэширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Функция для создания access токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    # Преобразуем "sub" в строку
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        print('не строка')
        to_encode["sub"] = str(to_encode["sub"])

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Функция для создания refresh токена
def create_refresh_token(data: dict):
    return create_access_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

# Функция для аутентификации пользователя по username и password
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

# Функция для логина (получение access и refresh токенов)
def login_user(db: Session, username: str, password: str, response: Response):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")

    access_token = create_access_token({"sub": user.id}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token({"sub": user.id})

    user.refresh_token = refresh_token
    db.commit()
    db.refresh(user)

    # Устанавливаем access токен в куки
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)

# Функция для обновления access токена через refresh токен
def refresh_access_token(db: Session, refresh_request: TokenRefreshRequest):
    try:
        payload = jwt.decode(refresh_request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate refresh token")

    user = db.query(User).filter(User.id == user_id, User.refresh_token == refresh_request.refresh_token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh-токен")

    access_token = create_access_token({"sub": user.id}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# Функция для проверки токена и извлечения информации о текущем пользователе
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id  # Возвращаем ID пользователя
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

# Функция для получения текущего пользователя по его ID
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")  # Получаем токен из куков
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token found in cookies")

    user_id = verify_access_token(token)  # Извлекаем ID пользователя из токена
    user = db.query(User).filter(User.id == user_id).first()  # Получаем пользователя по ID
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user  # Возвращаем текущего пользователя
