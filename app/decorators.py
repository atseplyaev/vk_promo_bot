from functools import wraps

from vkbottle.bot import Message
from vkbottle_types.objects import UsersUser
from .storage import context
import logging

logging.basicConfig(level=logging.INFO)


def user_context(func):
    """
    Подкладывает объект пользоваетля UsersUser в контекст функции
    """

    @wraps(func)
    async def wrapper(message: Message):
        cache_key = f'user_{message.from_id}'

        if context.contains(cache_key):
            user: UsersUser = context.get(cache_key)
        else:
            user: UsersUser = await message.get_user()
            context.set(cache_key, user)
        return await func(message, user)

    return wrapper
