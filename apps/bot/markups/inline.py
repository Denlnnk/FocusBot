from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.utils.callback_constants import DirectionCallBack
from apps.planner.models import WeekDay, TaskDirection


def week_day_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=day.label, callback_data=day.value)]
        for day in WeekDay
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def task_adding_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='Новое направление', callback_data='add_new_task'),
         InlineKeyboardButton(text='Выбрать из существующих', callback_data='choose_from_saved_tasks'), ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def user_task_direction_markup(users_directions: list[TaskDirection]) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=direction.title,
            callback_data=DirectionCallBack(call_back_name='user_direction', direction_title=direction.title).pack()
        )]
        for direction in users_directions
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
