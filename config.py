import logging
from logging.config import fileConfig
from pid import PidFile
import configparser
import asyncio
import sys
import os


configs_path = os.path.realpath(os.path.dirname(sys.argv[0])) + "/"


if not os.path.isfile(os.path.join(configs_path, "logging.ini")):
    raise FileExistsError(f"File logging.ini not found in path {configs_path}")

logging.config.fileConfig(os.path.join(configs_path, "logging.ini"), disable_existing_loggers=False)
log = logging.getLogger(__name__)


NAME = "quest"
TOKEN = "001.2918970001.1540231839:753423284"
ADMINS = ['77777777']

loop = asyncio.get_event_loop()

new_quest_list = [
    [{"text": "Добавить квест", "callbackData": "add_new_quest", "style": "attention"}], 
    [{"text": "Сделать рассылку", "callbackData": "mailing", "style": "attention"}]
]

message_quest_list = [
    [{"text": "Редактировать текст", "callbackData": "edit_text", "style": "attention"}], 
    [
        {"text": "Добавить кнопку", "callbackData": "add_button", "style": "attention"}, 
        {"text": "Добавить кнопку с задержкой", "callbackData": "add_button_sleep", "style": "attention"}
    ],
    [
        {"text": "Добавить кнопку с привязкой", "callbackData": "binding_button", "style": "attention"}, 
        {"text": "Удалить кнопки", "callbackData": "del_button", "style": "attention"}
    ],
    [{"text": "Перейти к сообщению", "callbackData": "go_message", "style": "attention"}]
] 

sleep_message_quest_list = [
    [{"text": "Редактировать текст", "callbackData": "edit_text", "style": "attention"}],
    [
        {"text": "Добавить сообщение", "callbackData": "add_message", "style": "attention"}, 
        {"text": "Добавить сообщение с задержкой", "callbackData": "add_message_sleep", "style": "attention"}
    ],    
    [
        {"text": "Добавить сообщение с привязкой", "callbackData": "add_message_binding", "style": "attention"},
        {"text": "Далее", "callbackData": "further", "style": "primary"},
    ],
    [{"text": "Перейти к сообщению", "callbackData": "go_message", "style": "attention"}]
]

standard_button_list = [
    [{"text": "На главную", "callbackData": "main"}],
    [{"text": "В начало сюжета", "callbackData": "start_quest"}]
]