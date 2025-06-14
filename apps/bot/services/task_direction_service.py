from asgiref.sync import sync_to_async

from apps.bot.models import TelegramUser
from apps.planner.models import TaskDirection


def _sync_get_or_create_direction(user: TelegramUser, title: str) -> TaskDirection:
    """
    Function for getting or creating TaskDirection instance
    """
    direction, _ = TaskDirection.objects.get_or_create(
        tg_user=user,
        title=title
    )
    return direction


get_or_create_direction = sync_to_async(_sync_get_or_create_direction, thread_sensitive=True)
