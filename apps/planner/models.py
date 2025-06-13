from django.db import models

from apps.bot.models import TelegramUser


class TaskDirection(models.Model):
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='task_directions')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WeekDay(models.TextChoices):
    MON = 'mon', 'Monday'
    TUE = 'tue', 'Tuesday'
    WED = 'wed', 'Wednesday'
    THU = 'thu', 'Thursday'
    FRI = 'fri', 'Friday'
    SAT = 'sat', 'Saturday'
    SUN = 'sun', 'Sunday'


class Task(models.Model):
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='tasks')
    task_direction = models.ForeignKey(TaskDirection, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    day_of_week = models.CharField(
        max_length=3,
        choices=WeekDay.choices,
        default=WeekDay.MON
    )
    time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskDetailStatus(models.TextChoices):
    IN_PROGRESS = 'in progress', 'In progress'
    MISSED = 'missed', 'Missed'
    MOVED = 'moved', 'Moved'
    DONE = 'done', 'Done'


class TaskDetail(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_details')
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=TaskDetailStatus.choices,
        default=TaskDetailStatus.IN_PROGRESS
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.task.title} — {self.date} — {self.status}"
