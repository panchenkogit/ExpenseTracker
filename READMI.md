ExpenseTracker — распределённый микросервисный проект на FastAPI для управления подписками, уведомлениями и кешированием данных с помощью Redis.

Стек технологий

Python 3.11+
FastAPI 0.115.8 — веб-фреймворк
Uvicorn 0.34.0 — ASGI-сервер
APScheduler 3.11.0 — планировщик фоновых задач
Redis 5.2.1 — хранилище для кеша
SQLAlchemy 2.0.38 + asyncpg 0.30.0 — асинхронный ORM для PostgreSQL
alembic 1.14.1 — миграции
bcrypt, passlib — хеширование паролей
pydantic 2.10.6 — валидация данных
aiosmtplib 4.0.1 — асинхронная отправка email
redis-py 5.2.1 — клиент Redis

Полный список зависимостей см. requirements.txt.

Микросервисы
1. user_service (порт 8000)
Функционал: регистрация, аутентификация, управление учетными записями пользователей.

Эндпоинты:

POST /auth/register — регистрация

POST /auth/login — получение JWT-токенов

POST /auth/logout — выход

JWT (access & refresh) в HTTP-only cookies

2. subscriber_service (порт 8001)

Функционал: CRUD-операции для подписок пользователя и запись напоминаний в Redis.

Эндпоинты:

POST /sub/create_new_sub — создание подписки (с вычислением даты следующего платежа)

PATCH /sub/update/{id} — обновление подписки (удаление старого и добавление нового напоминания)

DELETE /sub/delete/{id} — удаление подписки и соответствующего напоминания

GET /sub/get_all_subs — получение списка подписок пользователя

Особенности:

Вычисление даты платежа через dateutil.relativedelta (ежедневно, еженедельно, ежемесячно, ежегодно)

TTL-логику отложенных напоминаний реализует Redis Sorted Set (reminders)

3. notification_service (порт 8002)
Функционал: отправка email-уведомлений по расписанию.
Механизм:

APScheduler запускает задачу check_reminders по интервалу (например, каждые 5 мин).

Из Redis Sorted Set извлекаются все напоминания с score <= now.

Данные десериализуются в Pydantic-модель EmailReminder.

Отправка письма через aiosmtplib.

Удаление старого и пересоздание нового напоминания (с учётом частоты и уведомления за 3 дня).

Эндпоинты:

POST /send_notification — ручная отправка уведомления (для отладки)



🛠 Возможные проблемы и решения

Redis MISCONF (RDB snapshot failure)
Ошибка: MISCONF Redis is configured to save RDB snapshots...
Причина: Redis не мог записать dump.rdb в папку.
Решение: указали абсолютный путь dir D:/.../common_utils/redis/redis_data, создали папку и запустили Redis с этим конфигом; убрали старый процесс.

Сериализация объектов для Redis
Ошибка: Invalid input of type: 'EmailReminder' при zrem.
Решение: добавили метод to_dict() и всегда json.dumps(reminder.to_dict(), ensure_ascii=False) перед zadd/zrem.


🎯 Дальнейшие идеи для улучшения

Retry-логика с экспоненциальной задержкой  для отправки email

Очереди задач: выделить Celery + RabbitMQ для асинхронных задач и retry mechanism

Мониторинг: интеграция Prometheus + Grafana для отслеживания задержек и ошибок

Тесты: покрытие unit- и integration-тестами с pytest-asyncio

Интерфейс: минимальный веб-фронтенд (React/Vue) для управления подписками и просмотра логов уведомлений