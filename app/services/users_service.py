
from app.models import User, TrackedItem



async def get_or_register_user(user_vk_id: int, first_name: str, last_name: str) -> User:
    """
    Регистрирует пользователя в базе данных.

    Args:
        user_vk_id - vk id пользователя.
        first_name - фамилия пользователя.
        last_name - имя пользователя.

    Return:
        User - экземпляр класса пользователя.
    """
    user, _ = await User.get_or_create(vk_id=user_vk_id, first_name=first_name, last_name=last_name)

    return user



