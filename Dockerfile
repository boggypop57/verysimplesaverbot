FROM python:3.13.7-slim

WORKDIR /app

# Копируем сначала только requirements.txt для кэширования зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Запускаем бота
CMD ["python", "main.py"]