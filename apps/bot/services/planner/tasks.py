from datetime import time as time_type
from typing import Awaitable

from channels.db import database_sync_to_async

from apps.bot.models import TelegramUser
from apps.planner.models import Task
from apps.planner.models import TaskDirection


@database_sync_to_async
def get_or_update_task(
        user: TelegramUser, direction: TaskDirection, title: str, day_of_week: str, time: time_type
) -> Awaitable[Task]:
    """
    Function for getting or creating Task instance
    """
    task, _ = Task.objects.get_or_create(
        tg_user=user,
        task_direction=direction,
        title=title,
        day_of_week=day_of_week,
        defaults={
            "time": time,
            "is_active": True,
        }
    )
    return task
