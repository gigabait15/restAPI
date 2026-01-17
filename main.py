from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.base.schema import ResponseSchema
from core.database.session import engine
from seed import main as seed_main


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения FastAPI.

    Управляет ресурсами при старте и завершении приложения.
    При завершении закрывает соединения с базой данных.

    Args:
        app: Экземпляр FastAPI приложения.

    Yields:
        None: Приложение работает до завершения.
    """
    await seed_main()  # При старте: заполняем БД
    yield
    await engine.dispose()  # При завершении: закрываем соединения


app = FastAPI(
    title="REST API",
    version="0.1.0",
    lifespan=lifespan,
)

from api import activity, auth, organization  # noqa: E402

app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(activity.router)


@app.get("/health", response_model=ResponseSchema[dict[str, str]])
async def health_check() -> ResponseSchema[dict[str, str]]:
    """
    Проверка состояния здоровья сервиса.

    Returns:
        ResponseSchema[dict[str, str]]: Словарь со статусом "ok" если сервис работает.
    """
    return ResponseSchema(data=dict(status="ok"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
