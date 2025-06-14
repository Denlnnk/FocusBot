from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    task_direction = State()
    task_name = State()
    task_date = State()
    task_time = State()
