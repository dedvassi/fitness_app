from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    """
    Схема для передачи access и refresh токенов.
    """
    access_token: str = Field(..., description="JWT access-токен")
    refresh_token: str = Field(..., description="JWT refresh-токен")
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    """
    Схема для обновления access-токена через refresh-токен.
    """
    refresh_token: str = Field(..., description="JWT refresh-токен для обновления access-токена")
