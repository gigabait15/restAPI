import os
from pathlib import Path

from core.auth.api_key import generate_api_key
from core.base.config import settings

ENV_FILE = Path(".env")


def get_or_create_api_key() -> tuple[str, bool]:
    """
    Получить существующий или создать новый API ключ.

    Returns:
        tuple[str, bool]: (API ключ, True если создан новый).
    """
    try:
        existing_key = settings.API_KEY
        if existing_key:
            return existing_key, False
    except Exception:
        pass

    new_key = generate_api_key()
    save_api_key_to_env(new_key)
    return new_key, True


def save_api_key_to_env(api_key: str) -> None:
    """
    Сохранить API ключ в .env файл.

    Args:
        api_key: API ключ для сохранения.
    """
    if ENV_FILE.exists():
        content = ENV_FILE.read_text()
        lines = content.splitlines()
        new_lines = []
        key_found = False

        for line in lines:
            if line.startswith("API_KEY="):
                new_lines.append(f"API_KEY={api_key}")
                key_found = True
            else:
                new_lines.append(line)

        if not key_found:
            new_lines.append(f"API_KEY={api_key}")

        ENV_FILE.write_text("\n".join(new_lines) + "\n")
    else:
        ENV_FILE.write_text(f"API_KEY={api_key}\n")

    os.environ["API_KEY"] = api_key
