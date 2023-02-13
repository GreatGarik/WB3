import asyncio
import logging
import datetime
import random

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_data.config import Config, load_config
from handlers.user_handlers import register_user_handlers
from handlers.other_handlers import register_other_handlers
from keyboards.menu_button import set_main_menu
from parser.parser_get import parser

# from ids import USER_IDS, ADMIN_ID, KATERINA_ID

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция для регистрации всех хэндлеров
def register_all_handlers(dp: Dispatcher) -> None:
    register_other_handlers(dp)
    register_user_handlers(dp)


# Создаем экземпляр расписания
scheduler: AsyncIOScheduler = AsyncIOScheduler()


# Отправка сообщений в чат
async def send_message(dp, admin_id, katerina_id, slp=None):
    if slp:
        await asyncio.sleep(random.randint(0, 600))
    lst, lenkey = parser()
    if lst:
        for text in lst:
            await dp.bot.send_message(admin_id, text=text)
            await dp.bot.send_message(katerina_id, text=text)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot)

    # Отправка сообщения при запуске
    await send_message(dp, config.tg_bot.admin_id, config.tg_bot.katerina_id)

    # Добавляем функцию в расписание
    scheduler.add_job(send_message, "interval", hours=1,
                      args=(dp, config.tg_bot.admin_id, config.tg_bot.katerina_id, True))

    # Настраиваем кнопку Menu
    await set_main_menu(dp)

    # Регистрируем все хэндлеры
    register_all_handlers(dp)

    # Запускаем polling
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':

    try:
        # Запускаем функцию main
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
