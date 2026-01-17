from pydantic_settings import BaseSettings, SettingsConfigDict

EARTH_RADIUS_KM = 6371.0


class Settings(BaseSettings):
    """
    Конфигурация приложения.

    Загружает настройки из переменных окружения и файла .env.

    Attributes:
        DB_NAME: Название базы данных.
        DB_USER: Имя пользователя БД.
        DB_PASSWORD: Пароль пользователя БД.
        DB_HOST: Хост БД.
        DB_PORT: Порт БД.
        API_KEY: Ключ API для аутентификации.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    API_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Формирует URL для асинхронного подключения к PostgreSQL.

        Returns:
            str: URL подключения с драйвером asyncpg.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """
        Формирует URL для синхронного подключения к PostgreSQL.

        Returns:
            str: URL подключения с стандартным драйвером psycopg2.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()  # type: ignore[call-arg, call-overload]
