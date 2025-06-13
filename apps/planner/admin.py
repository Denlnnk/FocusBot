from django.contrib import admin

from apps.planner.models import TaskDirection, Task, TaskDetail


@admin.register(TaskDirection)
class TaskDirectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'tg_user')
    search_fields = ('title', 'tg_user__username', 'tg_user__full_name', 'tg_user__chat_id')
    autocomplete_fields = ('tg_user',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'day_of_week', 'task_direction', 'tg_user', 'is_active')
    search_fields = ('day_of_week', 'tg_user__username', 'tg_user__full_name', 'tg_user__chat_id')
    autocomplete_fields = ('tg_user', 'task_direction',)


@admin.register(TaskDetail)
class TaskDetailAdmin(admin.ModelAdmin):
    list_display = ('task', 'date', 'status')
    search_fields = ('task', 'date', 'status')
    autocomplete_fields = ('task',)
