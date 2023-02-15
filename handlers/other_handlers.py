from aiogram import Dispatcher, Router, F
from aiogram.types import Message
from ids import USER_IDS

router: Router = Router()

# Хэндлер для текстовых сообщений, которые отправляют незнакомцы.
@router.message(lambda message: message.from_user.id not in USER_IDS)
async def send_answer(message: Message):
    await message.answer(text='Я тебя не знаю, а мой создатель запретил мне разговаривать с незнакомцами!')