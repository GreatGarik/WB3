from aiogram import Dispatcher, types


# Функция для настройки кнопки Menu бота
async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/start', description='На старт!'),
        types.BotCommand(command='/help', description='Если хочешь узнать, что я делаю'),
       # types.BotCommand(command='/command_3', description='command_3 desription'),
        #types.BotCommand(command='/command_4', description='command_4 desription')
    ]
    await dp.bot.set_my_commands(main_menu_commands)