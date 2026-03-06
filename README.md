# URL Shortener

Сервис сокращения ссылок на FastAPI + PostgreSQL.

## 📖 О проекте

URL Shortener — это сервис для сокращения длинных ссылок. Сервис генерирует короткие уникальные идентификаторы на основе MD5-хеша с обработкой коллизий.

### Возможности

- ✅ Сокращение ссылок до 8 символов
- ✅ Редирект на оригинальный URL
- ✅ Подсчёт переходов
- ✅ Статистика по ссылке
- ✅ Проверка на дубликаты
- ✅ Обработка коллизий через соль

### Технологии

| Технология | Назначение |
|------------|------------|
| FastAPI | Веб-фреймворк |
| SQLAlchemy (async) | ORM |
| PostgreSQL | База данных |
| Alembic | Миграции |
| Pydantic | Валидация |
| Docker | Контейнеризация |
| pytest | Тестирование |

---

## 🚀 Запуск

### Через Docker Compose (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# Остановка
docker-compose down
```

Сервис доступен: http://localhost:8000

### Локальная разработка

```bash
# Установка зависимостей
uv sync

# Активация окружения
source .venv/bin/activate

# Применение миграций
alembic upgrade head

# Запуск сервера
uvicorn src.main:app --reload
```

---

## 🏗 Архитектура

```
src/
├── app/
│   ├── models.py       # SQLAlchemy модели
│   ├── repository.py   # Доступ к БД
│   ├── services.py     # Бизнес-логика
│   ├── schemas.py      # Pydantic схемы
│   └── routers.py      # API endpoints
├── routers/
│   └── api_router.py   # Основной роутер
├── settings/
│   └── settings.py     # Конфигурация
├── utils/
│   ├── database.py     # Подключение к БД
│   ├── dependencies.py # DI зависимости
│   ├── exceptions.py   # Исключения
│   └── hashurl_utils.py # Генерация short_url
├── tests/
│   ├── conftest.py     # Фикстуры
│   ├── test_hashurl_utils.py
│   ├── test_repository.py
│   └── test_services.py
└── main.py
```

### Слои приложения

```
┌─────────────────┐
│     Router      │ ← HTTP слой (FastAPI)
└────────┬────────┘
         ↓
┌─────────────────┐
│     Service     │ ← Бизнес-логика
└────────┬────────┘
         ↓
┌─────────────────┐
│    Repository   │ ← Доступ к БД
└────────┬────────┘
         ↓
┌─────────────────┐
│    Database     │ ← PostgreSQL
└─────────────────┘
```

### Dependency Injection

```python
# src/utils/dependencies.py
SessionDependency = Annotated[AsyncSession, Depends(get_session)]
RepositoryDependency = Annotated[URLRepository, Depends(get_repository)]
ServiceDependency = Annotated[URLService, Depends(get_service)]
```

**Цепочка:** `Endpoint → Service → Repository → Database`

---

## 📡 API

### POST /api/shorten

Сократить URL.

**Request:**
```bash
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/long"}'
```

**Response (201):**
```json
{
  "short_url": "a3f5c2d8",
  "original_url": "https://example.com/long",
  "redirect_count": 0
}
```

---

### GET /api/{short_id}

Редирект на оригинальный URL.

**Request:**
```bash
curl -I http://localhost:8000/api/a3f5c2d8
```

**Response (302):**
```
HTTP/1.1 302 Found
Location: https://example.com/long
```

---

### GET /api/stats/{short_id}

Статистика по ссылке.

**Request:**
```bash
curl http://localhost:8000/api/stats/a3f5c2d8
```

**Response (200):**
```json
{
  "short_url": "a3f5c2d8",
  "redirect_count": 42,
  "created_at": "2026-03-04T12:00:00"
}
```

---

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск по файлам
pytest src/tests/test_services.py -v
pytest src/tests/test_repository.py -v
pytest src/tests/test_hashurl_utils.py -v
```

### Структура тестов

| Файл | Тесты | Описание |
|------|-------|----------|
| `test_hashurl_utils.py` | 5 | Генерация short_url, коллизии |
| `test_repository.py` | 5 | CRUD операции с БД |
| `test_services.py` | 8 | Бизнес-логика, ошибки |
| **Всего** | **18** | **100% passed** |

### Фикстуры (conftest.py)

```python
mock_session      # mock SQLAlchemy сессии
mock_repository   # mock URLRepository
service           # URLService с mock repository
mock_url_model    # mock модели ShortURL
```

---

## ⚙️ Переменные окружения

### .env (локальный)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=urls_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

### .env.docker (для Docker)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=urls_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

---

## 🔧 Алгоритм сокращения

1. **Проверка дубликата** — если URL уже есть, возвращаем существующий short_url
2. **Генерация хеша** — MD5 от URL → первые 8 символов
3. **Проверка коллизии** — если short_url занят другим URL
4. **Добавление соли** — `url + random_salt` → новый хеш
5. **Сохранение в БД**

```python
# Пример
"https://example.com" → MD5 → "a3f5c2d8..."
Короткий URL: "a3f5c2d8"
```

---

## 📝 Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить
alembic downgrade -1
```

---
