from typing import Awaitable

from channels.db import database_sync_to_async

from apps.bot.models import TelegramUser
from apps.planner.models import TaskDirection


@database_sync_to_async
def get_or_create_direction(user: TelegramUser, title: str) -> Awaitable[TaskDirection]:
    """
    Function for getting or creating TaskDirection instance
    """
    direction, _ = TaskDirection.objects.get_or_create(
        tg_user=user,
        title=title
    )
    return direction


@database_sync_to_async
def check_user_directions_exists(user_chat_id: int) -> Awaitable[bool]:
    """
        Function for checking user TaskDirection instances
    """
    return TaskDirection.objects.filter(tg_user__chat_id=user_chat_id).exists()


@database_sync_to_async
def get_user_directions(user_chat_id: int) -> Awaitable[list[TaskDirection]]:
    """
        Function for retrieving user TaskDirection instances
    """
    return list(TaskDirection.objects.filter(tg_user__chat_id=user_chat_id))
