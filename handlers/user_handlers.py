from aiogram import Dispatcher
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU


# Этот хэндлер срабатывает на команду /start
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start_answer'])


# Этот хэндлер срабатывает на команду /help
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['help_answer'])

# # Хэндлер для текстовых сообщений, которые не попали в другие хэндлеры
async def answer_all(message: Message):
    await message.answer(text=LEXICON_RU['unknown_command'])


# Функция для регистрации хэндлеров в диспетчере. Вызывается в исполняемом файле bot.py
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands='start')
    dp.register_message_handler(process_help_command, commands='help')

    dp.register_message_handler(answer_all) # Ответ на неизвестные команды
