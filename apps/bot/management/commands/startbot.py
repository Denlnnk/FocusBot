import asyncio

from aiogram import Bot, Dispatcher
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.bot.handlers.command_handlers import command_router

bot: Bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(command_router)
    await dp.start_polling(bot)


class Command(BaseCommand):
    if settings.DEBUG:
        asyncio.run(main())
