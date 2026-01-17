from pydantic import BaseModel, Field


class TokenResponseSchema(BaseModel):
    """Схема ответа с API ключом."""

    api_key: str = Field(..., description="API ключ для авторизации")
    status: str = Field(..., description="Статус: created или existing")
    header_name: str = Field(
        default="X-API-Key", description="Имя заголовка для передачи ключа"
    )
