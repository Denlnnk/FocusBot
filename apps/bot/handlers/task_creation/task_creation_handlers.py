import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from apps.bot.markups.inline import week_day_inline_markup
from apps.bot.services.planner.directions import get_or_create_direction
from apps.bot.services.planner.tasks import get_or_update_task
from apps.bot.services.tg_user.tg_user import get_or_update_user
from apps.bot.states import AddTask
from apps.planner.models import WeekDay

task_creation_router = Router()


@task_creation_router.message(AddTask.task_direction)
async def _(message: Message, state: FSMContext):
    direction_title = message.text.strip()
    await state.update_data(direction_title=direction_title)
    await message.answer('Супер! Теперь пришли название задачи')
    await state.set_state(AddTask.task_name)


@task_creation_router.message(AddTask.task_name)
async def _(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text.strip())
    await message.answer(
        "Отлично! Выбери день недели для задачи:",
        reply_markup=week_day_inline_markup()
    )
    await state.set_state(AddTask.task_date)


@task_creation_router.callback_query(lambda c: c.data in {day.value for day in WeekDay})
async def _(call: CallbackQuery, state: FSMContext):
    day_code = call.data
    await state.update_data(day_of_week=day_code)

    await call.message.edit_text(
        f"Задача будет добавлена для: {WeekDay(day_code).label}\n\n"
        "Теперь укажи время задачи в формате HH:MM"
    )

    await state.set_state(AddTask.task_time)
    await call.answer()


@task_creation_router.message(AddTask.task_time)
async def _(message: Message, state: FSMContext):
    text = message.text.strip()
    try:
        time_obj = datetime.datetime.strptime(text, "%H:%M").time()
    except ValueError:
        await message.answer("Неверный формат времени. Формат: 19:30 или 08:05. Попробуй ещё раз.")
        return

    data = await state.get_data()
    direction_title = data["direction_title"]
    task_name = data["task_name"]
    day_code = data["day_of_week"]

    user = await get_or_update_user(message.from_user)
    direction = await get_or_create_direction(user, direction_title)

    await get_or_update_task(
        user=user,
        direction=direction,
        title=task_name,
        day_of_week=day_code,
        time=time_obj
    )

    day_label = WeekDay(day_code).label
    await message.answer(
        f"✅ Задача «{task_name}» добавлена на *{day_label}* в *{time_obj}*.",
        parse_mode="Markdown"
    )

    await state.clear()
