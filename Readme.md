[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![aiogram](https://img.shields.io/badge/aiogram-asyncio%20telegram-brightgreen)](https://aiogram.dev/)


# test_task_multibot
Бот, узнающий погоду, конвертирующий валюту, создающий опрос в чатах и присылающий
картинки милых котиков.
Написан на языке Python с использованием библиотеки aiogram. Запускается
в контейнере docker.

## Запуск
- Склонируйте репозиторий.
```
git clone https://github.com/elvir906/test_task_multibot.git
```

- Создайте в директории файл виртуального окружения .env и укажите в нём переменные:
```
TELEGRAM_TOKEN=<токен вашего бота>
GROUP_CHAT_ID=<id вашего группового чата>
APPID=<API ключ на сайте https://home.openweathermap.org/api_keys>
```

- Запустите контейнер командой 
```
docker-compose up -d --build
```


