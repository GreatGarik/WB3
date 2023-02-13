from aiogram import Dispatcher
from aiogram.types import Message
from ids import USER_IDS


# Хэндлер для текстовых сообщений, которые отправляют незнакомцы.
async def send_answer(message: Message):
    await message.answer(text='Я тебя не знаю, а мой создатель запретил мне разговаривать с незнакомцами!')


# Функция для регистрации хэндлера. Вызывается в исполняемом файле bot.py
def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(send_answer, lambda msg: msg.from_id not in USER_IDS)
