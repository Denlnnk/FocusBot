import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.bot.handlers.task_creation.utils.ai_transfrom_response import transform_ai_response_into_user_plan
from apps.bot.services.open_ai.open_ai import OpenAiService
from apps.bot.states import AiPlanCreation

plan_creation_router = Router()


@plan_creation_router.message(AiPlanCreation.plan_directions)
async def _(message: Message, state: FSMContext):
    plan_directions = message.text.strip()
    plan_directions = plan_directions.split(',')
    await state.update_data(plan_directions=plan_directions)
    await message.answer('Супер! Теперь пришли на сколько недель сгенерировать план')
    await state.set_state(AiPlanCreation.plan_weeks)


@plan_creation_router.message(AiPlanCreation.plan_weeks)
async def _(message: Message, state: FSMContext):
    plan_weeks = message.text.strip()
    # TODO Добавить проверку на то, чточ исло > 0 и добавить еще какое-то ограничение на максимальное число
    if not plan_weeks.isdigit():
        await message.answer('Пожалуйста, отправьте значение в виде числа')
        return

    state_data = await state.get_data()
    plan_directions = state_data['plan_directions']
    plan_weeks = int(plan_weeks)
    open_ai = OpenAiService('gpt-4.1-nano-2025-04-14')
    gen_task = asyncio.create_task(open_ai.generate_study_plan(
        directions=plan_directions,
        weeks=plan_weeks,
        answer_language='ru'
    ))

    status_msg = await message.answer("Generating.")
    dot_count = 1
    try:
        while not gen_task.done():
            dots = "." * dot_count
            try:
                await status_msg.edit_text(f"Generating{dots}")
            except Exception:
                pass
            dot_count = dot_count % 3 + 1  # 1→2→3→1
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        gen_task.cancel()
        raise

    await status_msg.delete()
    plan = await gen_task
    user_result_text = await transform_ai_response_into_user_plan(plan)
    await message.answer(user_result_text)
    await state.clear()
