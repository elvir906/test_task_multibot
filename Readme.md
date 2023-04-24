# test_task_multibot
Бот, узнающий погоду, конвертирующий валюту, создающий опрос в чатах и присылающий картинки милых котиков.

#Запуск
- Склонируйте репозиторий.
```
git clone https://github.com/elvir906/test_task_multibot.git
```

- Создайте файл виртуального окружения .env и укажите в нём переменные:
```
TELEGRAM_TOKEN=<токен вашего бота>
GROUP_CHAT_ID=<id вашего группового чата>
APPID=<API ключ на сайте https://home.openweathermap.org/api_keys>
```

- Запустите контейнер командой 
```
docker-compose up -d --build
```


