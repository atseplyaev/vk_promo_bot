from vkbottle import Keyboard, KeyboardButtonColor, Text
from app.models import User, TrackedItem

from app.utils import get_payload_command
from app import config


def get_main_keyboards(user: User) -> str:
    """
    Формирует и возварщает клавиатуру главного меню.

    Args:
        user: пользователь

    Returns:
        клавиатура главного меню.
    """
    if user.is_active:
        message: str = 'Деактивировать подписку'
        color: KeyboardButtonColor = KeyboardButtonColor.NEGATIVE
    else:
        message: str = 'Активировать подписку'
        color: KeyboardButtonColor = KeyboardButtonColor.POSITIVE

    keyboard: Keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text('Список отслеживаемых товаров (фраз)', get_payload_command('tracked_items_list', page=1)))
    keyboard.row()
    keyboard.add(Text(message, payload=get_payload_command('active_deactive_subscribe')), color=color)
    return keyboard.get_json()


async def get_tracked_items_keyboard(user: User, page: int = 1) -> str:
    """
    Формирует и возвращает клавиатуру списка отслеживаемых товаров.
    Args:
        user: пользователь
        page: текущая страница списка отслеживаемых товаров.

    Returns:
        клавиатура списка отслеживаемых товаров.
    """
    limit = config.TRACKED_ITEMS_COUNT_LIMIT
    offset = (page - 1) * limit if page > 1 else 0
    tracked_items = await user.trackeditems.all().values_list('id', 'phrase')
    count_tracked_items = await user.trackeditems.all().count()
    has_next_page: bool = count_tracked_items > offset + limit

    tracked_items = tracked_items[offset : offset + limit]

    keyboard: Keyboard = Keyboard(one_time=False, inline=False)
    for _id, phrase in tracked_items:
        keyboard.add(
            Text(
                phrase,
                payload=get_payload_command('tracked_item_details', tracked_item_id=_id, page=page),
            )
        )
        keyboard.row()

    if page > 1:
        keyboard.add(Text('Назад', payload=get_payload_command('tracked_items_list', page=page - 1)))

    keyboard.add(Text('Меню', payload=get_payload_command('main_menu')))

    if has_next_page:
        keyboard.add(Text('Вперёд', payload=get_payload_command('tracked_items_list', page=page + 1)))

    return keyboard.get_json()


async def get_tracked_item_menu(user: User, tracked_item: TrackedItem, page: int = 1) -> str:
    if tracked_item.is_active:
        message: str = 'Деактивировать отслеживаение фразы'
        color: KeyboardButtonColor = KeyboardButtonColor.NEGATIVE
    else:
        message: str = 'Активировать отслеживаение фразы'
        color: KeyboardButtonColor = KeyboardButtonColor.POSITIVE

    keyboard: Keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(
        Text(
            message,
            payload=get_payload_command('active_deactive_tracked_item', page=page, tracked_item_id=tracked_item.id),
        ),
        color=color,
    )
    keyboard.row()
    keyboard.add(
        Text(
            'Удалить фразу',
            payload=get_payload_command('delete_tracked_item', page=page, tracked_item_id=tracked_item.id),
        ),
        color=KeyboardButtonColor.NEGATIVE,
    )
    keyboard.row()
    keyboard.add(Text('Назад', payload=get_payload_command('tracked_items_list', page=page)))
    keyboard.row()

    keyboard.add(Text('Меню', payload=get_payload_command('main_menu')))
    return keyboard.get_json()
