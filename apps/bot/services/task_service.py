from datetime import time as time_type

from asgiref.sync import sync_to_async

from apps.bot.models import TelegramUser
from apps.planner.models import Task
from apps.planner.models import TaskDirection


def _sync_create_task_for_user(
        user: TelegramUser, direction: TaskDirection, title: str, day_of_week: str, time: time_type
) -> Task:
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


create_task_for_user = sync_to_async(_sync_create_task_for_user, thread_sensitive=True)
