# Используйте официальный образ Python
FROM python:3.9

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файлы проекта в контейнер
COPY . .

# Установите зависимости
RUN pip install -r requirements.txt

# Запускаем скрипт при старте контейнера
# docker run -p 80:80 -p 4444:4444  fastapi_with_st
RUN chmod +x start.sh
CMD ["./start.sh"]