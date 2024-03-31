# MOVC_project_tg_bot


# Установка

Создать `.env` файл и прописать в нём переменные окружения:
```commandline
API_TOKEN=...
```

Экспортирвоать переменные в окружение:
```commandline
export $(grep -v '^#' .env | xargs)
```

# Запуск тестов

Установка окуржения для тестов
```commandline
./prepare_tests_env.sh
```

Активация окружения для тестов
```commandline
source venv_tests/bin/activate
```

Запуск
```commandline
pytest
```

Ссылка на бота:
```
@Tom_and_Jerryy_bot
```