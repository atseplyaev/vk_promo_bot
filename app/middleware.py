from vkbottle import BaseMiddleware
from vkbottle.bot import Bot, Message
from vkbottle_types.objects import UsersUser

from .storage import context
from .models import User
from .services import get_or_register_user
from .types import UserContext


class RegistrationMiddleware(BaseMiddleware):
    """
    Middleware для регистрации пользователя
    """

    async def pre(self, message: Message) -> dict:
        cache_key = f'user_{message.from_id}'
        if context.contains(cache_key):
            cached_user: UserContext = context.get(cache_key)
        else:
            user_info: UsersUser = await message.get_user()
            user: User = await get_or_register_user(
                user_info.id, user_info.first_name, user_info.last_name
            )
            cached_user: UserContext = UserContext(user, user_info)

            context.set(cache_key, cached_user)
        return cached_user._asdict()
