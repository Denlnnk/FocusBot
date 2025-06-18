from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    task_direction = State()
    task_name = State()
    task_date = State()
    task_time = State()


class AiPlanCreation(StatesGroup):
    plan_directions = State()
    plan_weeks = State()
