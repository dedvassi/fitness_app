from fastapi import APIRouter
from app.auth.auth import *
from app.schemas.token import TokenSchema, TokenRefreshRequest
from app.schemas.user import UserCreate
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenSchema)
def register_user(user_create: UserCreate, response: Response, db: Session = Depends(get_db)):
    # Проверка, существует ли уже пользователь с таким именем
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким именем уже существует")

    # Хэшируем пароль
    hashed_password = get_password_hash(user_create.password)

    # Создаем нового пользователя с полными данными
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        age=user_create.age,
        weight=user_create.weight,
        height=user_create.height,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Генерация токенов
    access_token = create_access_token({"sub": new_user.id}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token({"sub": new_user.id})

    # Устанавливаем токены в куки
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)

    # Возвращаем токены
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenSchema)
def login(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    return login_user(db, username, password, response=response)


@router.post("/refresh", response_model=TokenSchema)
def refresh_token(refresh_request: TokenRefreshRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db, refresh_request)

@router.post("/logout")
def logout(response: Response, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.refresh_token = None
    db.commit()
    # Удаляем токен из куки
    response.set_cookie(key="access_token", value='', httponly=True, secure=True)
    return {"message": "Вы успешно вышли"}
