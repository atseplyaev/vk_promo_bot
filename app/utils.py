from typing import Set, Iterable
from functools import wraps
import json

from vkbottle_types.objects import UsersUser
from vkbottle.bot import Message

from .models import User


def get_payload_command(command: str, **kwargs) -> dict:
    """
    Обёртка над вызовом команды в payload хендлере.
    Params:
        command: комманда для вызова хендлера
        kwargs: необязательные аргументы.
    Return:
        payload для сообщения
    """
    payload = {'command': command}
    assert 'command' not in kwargs, '"command" args detected'
    payload.update(kwargs)

    return payload


def proxy_payload_args(args: Iterable[str]):
    """
    Проксирует аргументы из payload в хендлер
    Params:
        args: проксируемые аргументы
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, user: User, user_info: UsersUser):
            uniq_args = set(args)
            payload: dict = json.loads(message.payload)
            kwargs = {key: value for key, value in payload.items() if key in uniq_args}
            result = await func(message, user, user_info, **kwargs)
            return result

        return wrapper

    return decorator


CommandPayload = get_payload_command
