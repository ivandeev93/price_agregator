# Price Tracker

Учебный проект агрегатора цен.

Приложение позволяет добавлять товары по URL, отслеживать их текущую цену, сохранять историю изменений и автоматически проверять цены через фоновые задачи Celery.

Проект создан для практики:

- FastAPI
- async SQLAlchemy
- PostgreSQL
- Redis
- Celery
- Docker
- Web scraping
- Repository / Service архитектуры


## Возможности

- Добавление товаров для отслеживания
- Получение списка товаров
- Получение товара по ID
- Обновление информации о товаре
- Удаление товара
- Хранение истории изменения цен
- Кэширование запросов через Redis
- Фоновая проверка цен через Celery
- Автоматическая периодическая проверка товаров через Celery Beat
- Парсинг нескольких магазинов


## Поддерживаемые магазины

На данный момент реализованы парсеры:

- Kaspi
- Ozon
- Wildberries


## Технологии

Backend:

- Python 3.12
- FastAPI
- Pydantic v2
- SQLAlchemy Async


Database:

- PostgreSQL 16


Cache:

- Redis 7


Background tasks:

- Celery
- Celery Beat


Parsing:

- httpx
- BeautifulSoup4


Infrastructure:

- Docker
- Docker Compose


## Структура проекта


app/
│
├── core/
│ ├── config.py
│ ├── database.py
│ └── http.py
│
├── models/
│ ├── product.py
│ └── price_history.py
│
├── repositories/
│ ├── product_repository.py
│ └── price_history_repository.py
│
├── routers/
│ └── product.py
│
├── schemas/
│ ├── product.py
│ ├── price_history.py
│ └── parser.py
│
├── services/
│ ├── product_service.py
│ ├── price_history_service.py
│ ├── parser_service.py
│ │
│ └── parsers/
│ ├── base.py
│ ├── kaspi.py
│ ├── ozon.py
│ └── wildberries.py
│
├── tasks/
│ ├── price_tasks.py
│ └── scheduler_tasks.py
│
├── utils/
│ └── cache.py
│
├── worker/
│ └── celery_app.py
│
├── main.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


# Запуск проекта

## 1. Клонирование проекта

```bash
git clone <repository_url>

cd price-tracker


## Пример .env

APP_NAME=Price Tracker

DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/pricetracker

REDIS_URL=redis://redis:6379/0

CACHE_EXPIRE_SECONDS=300

CELERY_BROKER_URL=redis://redis:6379/1

CELERY_RESULT_BACKEND=redis://redis:6379/2