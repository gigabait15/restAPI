from fastapi import APIRouter

from core.auth.schema import TokenResponseSchema
from core.auth.service import get_or_create_api_key
from core.base.schema import ResponseSchema

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)


@router.get("/token", response_model=ResponseSchema[TokenResponseSchema])
async def get_token() -> ResponseSchema[TokenResponseSchema]:
    """
    Получить API ключ.

    Если ключ не существует в .env — генерирует новый и сохраняет.
    Если существует — возвращает текущий.

    Returns:
        ResponseSchema[TokenResponseSchema]: API ключ и статус (created/existing).
    """
    api_key, is_new = get_or_create_api_key()
    return ResponseSchema(
        data=TokenResponseSchema(
            api_key=api_key,
            status="created" if is_new else "existing",
            header_name="X-API-Key",
        )
    )
