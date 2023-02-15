from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command='/start',
        description='На старт!'),
        BotCommand(
            command='/help',
            description='Если хочешь узнать, что я делаю')]
    await bot.set_my_commands(main_menu_commands)

'''
    main_menu_commands = [
        types.BotCommand(command='/start', description='На старт!'),
        types.BotCommand(command='/help', description='Если хочешь узнать, что я делаю'),
       # types.BotCommand(command='/command_3', description='command_3 desription'),
        #types.BotCommand(command='/command_4', description='command_4 desription')
    ]
    await dp.register_message_handler(main_menu_commands)
'''