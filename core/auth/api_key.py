import secrets
from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from core.base.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

__all__ = ("APIKey", "generate_api_key")


def generate_api_key() -> str:
    """Генерация нового API ключа (использовать один раз для .env)."""
    return secrets.token_urlsafe(32)


class APIKey:
    """Класс для аутентификации по API ключу."""

    def __init__(self):
        """Инициализация с загрузкой API ключа из настроек."""
        self.api_key = settings.API_KEY

    def verify(self, api_key: str) -> bool:
        """
        Проверка валидности API ключа.

        Использует безопасное сравнение строк для защиты от timing attacks.

        Args:
            api_key: Проверяемый API ключ.

        Returns:
            bool: True если ключ валиден, False в противном случае.
        """
        return secrets.compare_digest(api_key, self.api_key)

    async def __call__(
        self,
        api_key: Annotated[str | None, Security(api_key_header)],
    ) -> str:
        """
        Dependency для FastAPI для проверки API ключа в заголовке запроса.

        Args:
            api_key: API ключ из заголовка X-API-Key.

        Returns:
            str: Валидный API ключ.

        Raises:
            HTTPException: 401 если ключ не предоставлен, 403 если ключ неверный.
        """
        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API ключ не предоставлен",
            )

        if not self.verify(api_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Неверный API ключ",
            )

        return api_key


api_key_auth = APIKey()
