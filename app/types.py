from typing import NamedTuple
from vkbottle_types.objects import UsersUser
from .models import User


class UserContext(NamedTuple):
    """ Структура хранения пользователя в контексте """

    user: User
    user_info: UsersUser
