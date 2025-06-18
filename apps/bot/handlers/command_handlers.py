from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.bot.markups.inline import task_adding_markup
from apps.bot.services.planner.directions import check_user_directions_exists
from apps.bot.states import AddTask, AiPlanCreation
from apps.bot.utils.decorators import track_user_data

command_router = Router()


@command_router.message(CommandStart())
@track_user_data
async def _(message: Message):
    user_info = message.from_user
    start_text = (
        f'Привет 👋 {user_info.first_name}'
        f'\nЯ помогу тебе составить план и напоминать о задачах.'
        f'\nГотов начать?'
    )
    await message.answer(start_text)


@command_router.message(Command('add'))
@track_user_data
async def _(message: Message, state: FSMContext):
    if await check_user_directions_exists(message.from_user.id):
        await message.answer(
            'Создадим новое направление или выберем из существующих?', reply_markup=task_adding_markup()
        )
        return

    await message.answer(
        'Какое направление будет у задачи?(например: English, Self Education и тд)'
    )
    await state.set_state(AddTask.task_direction)


@command_router.message(Command('plan_creation'))
@track_user_data
async def _(message: Message, state: FSMContext):
    answer_text = (
        'По каким направлениям желаете сгенерировать план?'
        '\nПример: English, Self Education'
        '\n<b>Важно!</b>: направления перечислять через запятую'
    )
    await message.answer(answer_text, parse_mode='html')
    await state.set_state(AiPlanCreation.plan_directions)
