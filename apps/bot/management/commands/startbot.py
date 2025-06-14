import asyncio

from aiogram import Bot, Dispatcher
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.bot.handlers.command_handlers import command_router
from apps.bot.handlers.task_creation.task_creation_handlers import task_creation_router

bot: Bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(command_router, task_creation_router)
    await dp.start_polling(bot)


class Command(BaseCommand):
    if settings.DEBUG:
        asyncio.run(main())
