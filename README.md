# Квестики

# Оглавление 
 - [Описание](https://github.com/ICQ-BOTS/quest_bot#описание)
 - [Установка](https://github.com/ICQ-BOTS/quest_bot#установка)
 - [Скриншоты работы](https://github.com/ICQ-BOTS/quest_bot#скриншоты-работы)

# Описание
Бот для создание квестов!

# Установка

1. Установка всех зависимостей 
```bash
pip install -r requirements.txt
```

2. Запуск space tarantool
```bash
tarantoolctl start quest.lua
```
> Файл из папки scheme нужно перекинуть в /etc/tarantool/instances.available

4. Вставляем токен, ид админов в config.bot
> Активация админки в боте командой /admin


5. Запуск бота!
```bash
python3 quest_bot.py
```

# Скриншоты работы
<img src="https://github.com/ICQ-BOTS/quest_bot/blob/main/img/1.png" width="400">
<img src="https://github.com/ICQ-BOTS/quest_bot/blob/main/img/2.png" width="400">