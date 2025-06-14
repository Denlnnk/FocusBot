from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from apps.bot.utils.decorators import track_user_data

command_router = Router()


@command_router.message(CommandStart())
@track_user_data
async def _(message: Message):
    user_info = message.from_user
    start_text = (
        f'Привет 👋 {user_info.first_name}'
        f'\nЯ помогу тебе составить план и напоминать о задачах.'
        f'\nГотов начать?'
    )
    await message.answer(start_text)
