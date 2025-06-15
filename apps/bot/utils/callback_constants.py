from aiogram.filters.callback_data import CallbackData

class DirectionCallBack(CallbackData, prefix='direction_'):
    call_back_name: str
    direction_title: str
