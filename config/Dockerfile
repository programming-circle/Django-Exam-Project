# 1. Базовый образ: берем официальный Python нужной версии
FROM python:3.11-slim

# 2. Настройка среды: запрещаем Python писать файлы .pyc и буферизировать вывод (актуально для логов Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Создаем рабочую директорию внутри контейнера, где будет жить наш код
WORKDIR /app

# 4. Сначала копируем только файл зависимостей (это ускоряет повторную сборку образа)
COPY requirements.txt /app/

# 5. Обновляем pip и устанавливаем все библиотеки из requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Копируем абсолютно весь оставшийся код вашего Django-проекта в контейнер
COPY . /app/

# 7. Открываем порт 8000 (на нем обычно крутится Django) наружу контейнера
EXPOSE 8000

# 8. Команда, которая выполнится при запуске контейнера: стартуем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]