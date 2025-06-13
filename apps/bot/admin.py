from django.contrib import admin

from apps.bot.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user_contact_details', 'status')
    search_fields = ('username', 'full_name', 'chat_id')
    readonly_fields = ('created_at', 'updated_at')