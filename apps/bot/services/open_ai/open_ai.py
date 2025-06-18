import json
import time
from pprint import pprint

from asgiref.sync import sync_to_async
from django.conf import settings
from openai import OpenAI


class OpenAiService:

    def __init__(self, model):
        self.model = model
        self.client = OpenAI(api_key=settings.OPEN_AI_TOKEN)

    @sync_to_async(thread_sensitive=True)
    def generate_study_plan(self, directions: list[str], weeks: int, answer_language: str) -> dict:
        # TODO пересмотреть, может переписать на асинхронную функцию + ПОИГРАТЬСЯ с результатом от чата, пока ответ не идеален
        system_prompt = self._get_system_focus_bot_prompt(answer_language)
        user_prompt = self._get_user_focus_bot_prompt(directions, weeks)

        week_schema = {
            "type": "object",
            "properties": {
                day: {"type": "array", "items": {"type": "string"}}
                for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            },
            "required": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        }
        functions = [{
            "name": "generate_study_plan",
            "description": "Generate a multi-week study plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    f"week_{i + 1}": week_schema
                    for i in range(weeks)
                },
                "required": [f"week_{i + 1}" for i in range(weeks)]
            }
        }]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self._make_request_to_open_ai(messages, functions, function_call={"name": "generate_study_plan"})

        msg = response.choices[0].message
        plan = json.loads(msg.function_call.arguments)
        return plan

    def _make_request_to_open_ai(self, messages: list[dict], functions, function_call):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call=function_call,
            temperature=0.7,
        )

    @staticmethod
    def _get_system_focus_bot_prompt(answer_language: str) -> str:
        system_prompt = (
            "You are FocusBot, a Telegram study-plan assistant. "
            "Given directions and number of weeks, you MUST return a JSON object "
            "with keys 'week_1', 'week_2', … each containing days Monday–Sunday, "
            "and for each day a list of short task descriptions."
            f"Your answer MUST be in {answer_language} language"
        )
        return system_prompt

    @staticmethod
    def _get_user_focus_bot_prompt(directions: list[str], weeks: int) -> str:
        lines = "\n".join(f"- {d}" for d in directions)
        return (
            f"Create a plan for {weeks} weeks.\n"
            f"Directions:\n{lines}"
        )


if __name__ == '__main__':
    open_ai_service = OpenAiService('gpt-4.1-nano-2025-04-14')
    directions = ['IT education', 'English']
    weeks = 4
    plan = open_ai_service.generate_study_plan(directions, weeks, 'ru')
    pprint(plan)
