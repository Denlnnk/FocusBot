from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.planner.models import WeekDay

def week_day_inline_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=day.label, callback_data=day.value)]
        for day in WeekDay
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
