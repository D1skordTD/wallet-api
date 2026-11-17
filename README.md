# Wallet API

REST API для управления балансом кошельков (DEPOSIT / WITHDRAW).

## Стек

- FastAPI (async)
- PostgreSQL + SQLAlchemy (async, asyncpg)
- Alembic (миграции)
- pytest + httpx (тесты)
- Docker / docker-compose

## Запуск

```
docker-compose up --build
```

Поднимет базу данных и приложение, миграции применятся автоматически.
API будет доступно на `http://localhost:8000`.

## Эндпоинты

- `POST /api/v1/wallets/{wallet_id}/operation` — выполнить операцию

- `GET /api/v1/wallets/{wallet_id}` — получить баланс кошелька