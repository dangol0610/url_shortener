# URL Shortener

Сервис сокращения ссылок (аналог bitly) на FastAPI + PostgreSQL.

## Возможности

- ✅ Сокращение длинных ссылок до 8 символов
- ✅ Редирект на оригинальную ссылку по короткому идентификатору
- ✅ Подсчёт количества переходов по каждой ссылке
- ✅ Проверка на дубликаты (одинаковый URL → одинаковый short_id)
- ✅ Обработка коллизий через добавление соли

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy (async)** — ORM для работы с БД
- **PostgreSQL** — база данных
- **Alembic** — миграции БД
- **Pydantic** — валидация данных
- **Docker + Docker Compose** — контейнеризация

## Архитектура

```
src/
├── app/
│   ├── models.py       # SQLAlchemy модели
│   ├── repository.py   # Работа с БД
│   ├── services.py     # Бизнес-логика
│   ├── schemas.py      # Pydantic схемы
│   └── routers.py      # API эндпоинты
├── routers/
│   └── api_router.py   # Основной роутер
├── settings/
│   └── settings.py     # Настройки приложения
├── utils/
│   ├── database.py     # Подключение к БД
│   ├── dependencies.py # DI зависимости
│   ├── exceptions.py   # Кастомные исключения
│   └── hashurl_utils.py # Утилиты для генерации short_url
├── tests/              # Тесты
└── main.py             # Точка входа
```

## API Endpoints

### POST /api/shorten

Сократить URL.

**Request:**
```json
{
    "url": "https://example.com/very/long/path?param=value"
}
```

**Response:**
```json
{
    "short_id": "a3f5c2d8",
    "original_url": "https://example.com/very/long/path?param=value",
    "redirect_count": 0
}
```

---

### GET /api/{short_id}

Редирект на оригинальную ссылку.

**Request:**
```
GET /api/a3f5c2d8
```

**Response:**
```
HTTP/1.1 302 Found
Location: https://example.com/very/long/path?param=value
```

---

### GET /api/stats/{short_id}

Получить статистику по ссылке.

**Request:**
```
GET /api/stats/a3f5c2d8
```

**Response:**
```json
{
    "short_id": "a3f5c2d8",
    "original_url": "https://example.com/very/long/path?param=value",
    "redirect_count": 42,
    "created_at": "2026-03-04T12:00:00"
}
```

---

## Запуск

### Через Docker Compose (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# Остановка
docker-compose down
```

Сервис доступен по адресу: http://localhost:8000

### Локальная разработка

```bash
# Установка зависимостей
uv sync

# Активация виртуального окружения
source .venv/bin/activate

# Запуск миграций
alembic upgrade head

# Запуск сервера
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Переменные окружения

Файл `.env` (локальный) и `.env.docker` (для Docker):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=urls_db
POSTGRES_HOST=localhost      # или postgres для Docker
POSTGRES_PORT=5433           # или 5432 для Docker
```

## Тесты

```bash
# Запуск тестов
pytest

# Запуск с покрытием
pytest --cov=src
```

## Алгоритм сокращения ссылок

1. Проверяем, нет ли уже такой ссылки в БД (детерминированность)
2. Генерируем MD5 хеш от URL → первые 8 символов
3. Проверяем на коллизию с другими URL
4. Если коллизия → добавляем случайную соль и хешируем снова
5. Сохраняем в БД

**Пример:**
```
"https://example.com" → MD5 → "a3f5c2d8..."
Короткий URL: "a3f5c2d8"
```

## Production-особенности

### Обработка коллизий

При коллизии хешей добавляется случайная соль:

```python
salted = url + secrets.token_hex(4)
short_url = hashlib.md5(salted.encode()).hexdigest()[:8]
```

### Dependency Injection

Используется многослойный DI:

```
Endpoint → Service → Repository → Database
```

Каждый слой получает зависимости через `Depends()`.

### Асинхронность

Все операции с БД асинхронные через `asyncpg`.

## Лицензия

MIT
