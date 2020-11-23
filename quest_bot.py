from config import *
from handlers import *
from mailru_im_async_bot.filter import Filter
from mailru_im_async_bot.bot import Bot
from mailru_im_async_bot.handler import MessageHandler, CommandHandler, DefaultHandler, StartCommandHandler, BotButtonCommandHandler

bot = Bot(token=TOKEN, name=NAME)

# Register your handlers here
# ---------------------------------------------------------------------
bot.dispatcher.add_handler(CommandHandler(
        callback=admin, 
        command='admin'
    )
)
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=add_new_quest,
                            filters=Filter.callback_data('add_new_quest')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=edit_text,
                            filters=Filter.callback_data('edit_text')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=add_button,
                            filters=Filter.callback_data('add_button')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=del_button,
                            filters=Filter.callback_data('del_button')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=go_message,
                            filters=Filter.callback_data('go_message')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=binding_button,
                            filters=Filter.callback_data('binding_button')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=add_button_sleep,
                            filters=Filter.callback_data('add_button_sleep')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=main,
                            filters=Filter.callback_data('main')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=start_quest,
                            filters=Filter.callback_data('start_quest')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=further,
                            filters=Filter.callback_data('further')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=add_message_bot,
                            filters=Filter.callback_data('add_message')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=add_message_sleep,
                            filters=Filter.callback_data('add_message_sleep')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=add_message_binding,
                            filters=Filter.callback_data('add_message_binding')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=mailing,
                            filters=Filter.callback_data('mailing')
                        )
                    )
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=message_quest,
                            filters=Filter.callback_data_regexp('^message')
                        )
                    )        
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=sleep_message,
                            filters=Filter.callback_data_regexp('^sleepMessage')
                        )
                    )  
bot.dispatcher.add_handler(BotButtonCommandHandler(
                            callback=public_quest,
                            filters=Filter.callback_data_regexp('^public')
                        )
                    )                                              
bot.dispatcher.add_handler(MessageHandler(
                            callback=default_command
                        )
                    )


with PidFile(NAME):
    try:
        loop.create_task(bot.start_polling())
        loop.run_forever()
    finally:
        loop.close()
