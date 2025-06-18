async def transform_ai_response_into_user_plan(ai_response: dict) -> str:
    """
        Transform ai response into user plan
        Ai response structure:
            {'week_1': {'day1': ['plan1', 'plan2', 'plan3'], 'day2': ['plan4', 'plan5', 'plan6']}...},
            {'week_2': {'day1': ['plan1', 'plan2', 'plan3'], 'day2': ['plan4', 'plan5', 'plan6']}...}
    """
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    lines: list[str] = []
    for week_key in sorted(ai_response.keys(), key=lambda k: int(k.split('_')[1])):
        week_num = int(week_key.split('_')[1])
        lines.append(f"📅 Неделя {week_num}:")

        week_data = ai_response[week_key]
        for day in weekdays:
            tasks = week_data.get(day)
            if not tasks:
                continue

            lines.append(f"{day}:")
            for t in tasks:
                lines.append(f"  – {t}")

        lines.append("")

    return "\n".join(lines).strip()
