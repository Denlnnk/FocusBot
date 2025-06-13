from django.db import models
from django.utils import timezone


class TelegramUserStatus(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    DEFAULT = 'default', 'Default'
    DISABLED = 'disabled', 'Disabled'
    UNAUTHORIZED = 'unauthorized', 'Unauthorized'


class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=TelegramUserStatus.choices, default=TelegramUserStatus.UNAUTHORIZED
    )
    last_active_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or self.full_name or str(self.chat_id)
