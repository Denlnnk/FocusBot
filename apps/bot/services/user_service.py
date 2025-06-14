from asgiref.sync import sync_to_async
from django.utils import timezone

from apps.bot.models import TelegramUser, TelegramUserStatus


def _sync_get_or_update_user(tg_user) -> None:
    """
    Function for saving or updating TelegramUser instance
    """
    tg_user_full_name = f'{tg_user.first_name} {tg_user.last_name}'.strip()
    obj, created = TelegramUser.objects.get_or_create(
        chat_id=tg_user.id,
        defaults={
            "username": tg_user.username,
            "full_name": tg_user_full_name,
            "last_active_time": timezone.now(),
            "status": TelegramUserStatus.BASIC,
        }
    )

    if not created:
        if obj.username != tg_user.username:
            obj.username = tg_user.username

        if obj.full_name != tg_user_full_name:
            obj.full_name = tg_user_full_name

        obj.last_active_time = timezone.now()
        obj.save()


get_or_update_user = sync_to_async(_sync_get_or_update_user, thread_sensitive=True)
