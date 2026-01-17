# REST API Test

REST API на FastAPI для работы с организациями, зданиями и видами
деятельности. При старте приложение автоматически очищает и заполняет БД
тестовыми данными.

## Возможности

- Поиск организаций по адресу здания, названию, виду деятельности.
- Поиск по иерархии видов деятельности (включая дочерние).
- Гео‑поиск по радиусу и по прямоугольным границам.
- API‑ключ для доступа к защищённым эндпоинтам.
- OpenAPI документация в `/docs` и `/redoc`.

## Технологии

- Python 3.12, FastAPI
- SQLAlchemy (async), PostgreSQL
- Uvicorn
- Docker / Docker Compose

## Структура проекта

```
.
├── api/                 # HTTP роуты (FastAPI routers)
│   ├── activity.py      # Эндпоинты по видам деятельности
│   ├── auth.py          # Получение API‑ключа
│   └── organization.py  # Эндпоинты по организациям
├── app/                 # Доменная логика и схемы
│   ├── activity/         # CRUD/модели/сервисы для деятельности
│   ├── building/         # CRUD/модели/сервисы для зданий
│   └── organization/     # CRUD/модели/сервисы для организаций
├── core/                # Базовая инфраструктура
│   ├── auth/             # API‑ключ и auth‑helpers
│   ├── base/             # Конфиг, схемы ответов, логгер
│   └── database/         # Сессии и общие DB‑утилиты
├── migrations/          # Alembic миграции
├── seed.py              # Начальный сидинг тестовых данных
├── main.py              # Точка входа FastAPI
├── Dockerfile           # Образ приложения
├── docker-compose.yml   # Compose для API + Postgres
├── pyproject.toml       # Зависимости и метаданные проекта
└── uv.lock              # Lockfile для uv
```

## Переменные окружения

Приложение читает конфигурацию из `.env`:

```
DB_NAME=restapi
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
API_KEY=
```

`API_KEY` может быть пустым — тогда его можно сгенерировать через
`/api/v1/auth/token`, и он сохранится в `.env`.

## Запуск локально

1) Установите зависимости через `uv`:

```
uv sync
```

2) Запустите PostgreSQL (локально или через Docker) и создайте `.env`.

3) Запустите приложение:

```
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API будет доступен по адресу `http://localhost:8000`.

## Запуск через Docker

Сборка и запуск:

```
docker-compose up -d --build
```

Сервисы:
- API: `http://localhost:8000`
- Postgres проброшен на хост: `localhost:5433`

Логи приложения:

```
docker-compose logs -f app
```

## Быстрый старт API

Получить API‑ключ:

```
curl http://localhost:8000/api/v1/auth/token
```

Использовать ключ (заголовок `X-API-Key`):

```
curl -H "X-API-Key: <ключ>" \
  http://localhost:8000/api/v1/organization/name/%D0%9E%D0%9E%D0%9E%20%22%D0%A0%D0%BE%D0%B3%D0%B0%20%D0%B8%20%D0%9A%D0%BE%D0%BF%D1%8B%D1%82%D0%B0%22
```

Примеры эндпоинтов:
- `GET /api/v1/organization/{id}`
- `GET /api/v1/organization/name/{name}`
- `GET /api/v1/organization/activity/{activity_name}`
- `GET /api/v1/organization/activity-tree/{activity_name}`
- `GET /api/v1/organization/building/{building_address}`
- `GET /api/v1/organization/geo/radius?lat=...&lon=...&radius_km=...`
- `GET /api/v1/organization/geo/bounds?min_lat=...&min_lon=...&max_lat=...&max_lon=...`
- `POST /api/v1/activity/set-max-level`
- `GET /health`

## Использование и авторизация

Документация доступна:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Для всех защищённых эндпоинтов требуется API‑ключ. Передавайте его в заголовке
`X-API-Key`:

```
X-API-Key: <ваш_ключ>
```

Если ключ не задан в `.env`, можно получить его через `/api/v1/auth/token` —
ключ будет сгенерирован и сохранён в `.env`.

### Использование ключа в Swagger UI

В Swagger UI нажмите кнопку **Authorize** и вставьте ключ в поле для
`X-API-Key` (без префикса `Bearer`). После авторизации все запросы из UI
будут автоматически отправляться с этим заголовком.
