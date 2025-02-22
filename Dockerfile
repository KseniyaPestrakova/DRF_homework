# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

RUN pip install poetry

# Устанавливаем переменные окружения для poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости Python
RUN poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Определяем переменные окружения
ENV SECRET_KEY="SECRET_KEY"
ENV CELERY_BROKER_URL="CELERY_BROKER_URL"
ENV CELERY_BACKEND="CELERY_RESULT_BACKEND"

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]