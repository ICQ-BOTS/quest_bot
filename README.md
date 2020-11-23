# Квестики

Старт:
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
