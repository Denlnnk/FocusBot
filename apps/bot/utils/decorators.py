from functools import wraps

from apps.bot.services.user_service import get_or_update_user


def track_user_data(handler):
    @wraps(handler)
    async def wrapper(event, *args, **kwargs):
        if hasattr(event, 'from_user'):
            await get_or_update_user(event.from_user)
        return await handler(event, *args, **kwargs)

    return wrapper
