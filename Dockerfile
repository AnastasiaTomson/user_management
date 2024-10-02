# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y gcc python3-dev musl-dev

# Копируем файлы requirements.txt
COPY requirements.txt /app/

# Устанавливаем зависимости проекта
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Открываем порт для приложения
EXPOSE 8000

# Выполняем миграции и запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0:8000"]
