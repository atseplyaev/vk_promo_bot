from vkbottle.bot import Blueprint, Message, BotLabeler, rules
from vkbottle_types.objects import UsersUser

from vkbottle import Callback, GroupEventType, GroupTypes, Keyboard, Text
from app.models import User, TrackedItem
from app.services import get_main_keyboards, get_tracked_items_keyboard, get_tracked_item_menu
from app.utils import CommandPayload, proxy_payload_args

bp = Blueprint()


@bp.on.message(payload=CommandPayload('start'))
async def start_communication_handler(message: Message, user: User, user_info: UsersUser):
    await message.answer('Меню', keyboard=get_main_keyboards(user))


@bp.on.message(payload=CommandPayload('main_menu'))
async def main_menu_handler(message: Message, user: User, user_info: UsersUser):
    await message.answer('Меню', keyboard=get_main_keyboards(user))


@bp.on.message(payload=CommandPayload('active_deactive_subscribe'))
async def active_deactive_subscribe_handler(message: Message, user: User, user_info: UsersUser):
    user.is_active = not user.is_active
    await user.save(update_fields=['is_active'])
    msg = 'деактивирована'

    if user.is_active:
        msg = 'активирована'

    await message.answer(f'Подписка {msg}', keyboard=get_main_keyboards(user))


@bp.on.message(payload_contains=CommandPayload('tracked_items_list'))
@proxy_payload_args(('page',))
async def tracked_items_list_handler(message: Message, user: User, user_info: UsersUser, page: int):
    """ Хендлер получения меню с отслеживаемыми товарами """
    await message.answer(
        'Список отслеживаемых товаров', keyboard=await get_tracked_items_keyboard(user, page)
    )


@bp.on.message(payload_contains=CommandPayload('tracked_item_details'))
@proxy_payload_args(('tracked_item_id', 'page'))
async def tracked_item_details_handler(
    message: Message, user: User, user_info: UsersUser, tracked_item_id: int, page: int
):
    """ Хендлер для работы с одним отслеживаемым товаром """
    tracked_item: TrackedItem = await user.trackeditems.filter(id=tracked_item_id).first()
    keyboard = await get_tracked_item_menu(user, tracked_item, page)
    await message.answer(tracked_item.phrase, keyboard=keyboard)


@bp.on.message(payload_contains=CommandPayload('active_deactive_tracked_item'))
@proxy_payload_args(('tracked_item_id', 'page'))
async def active_deactive_tracked_item_handler(
    message: Message, user: User, user_info: UsersUser, tracked_item_id: int, page: int
):
    """ Хендлер для активации/деактивации отслеживамого товара """
    tracked_item: TrackedItem = await user.trackeditems.filter(id=tracked_item_id).first()
    tracked_item.is_active = not tracked_item.is_active
    await tracked_item.save(update_fields=['is_active'])
    msg = 'Фраза {phrase} {status}'

    if tracked_item.is_active:
        status = 'Активирована'
    else:
        status = 'Деактивирована'
    msg = msg.format(phrase=tracked_item.phrase, status=status)
    keyboard = await get_tracked_item_menu(user, tracked_item, page)
    await message.answer(msg, keyboard=keyboard)


@bp.on.message(payload_contains=CommandPayload('delete_tracked_item'))
@proxy_payload_args(('tracked_item_id', 'page'))
async def delete_tracked_item_handler(
    message: Message, user: User, user_info: UsersUser, tracked_item_id: int, page: int
):
    """ Хендлер для удаления отслеживамого товара """
    tracked_item: TrackedItem = await user.trackeditems.filter(id=tracked_item_id).first()
    tracked_item_phrase = tracked_item.phrase
    await user.trackeditems.filter(id=tracked_item_id).delete()
    await message.answer(
        f'Фраза "{tracked_item_phrase}" удалена',
        keyboard=await get_tracked_items_keyboard(user, page),
    )


@bp.on.message((rules.RegexRule('Добавить фразу (.*)')))
async def add_tracked_item_handler(message: Message, user: User, user_info: UsersUser, match):
    """ Хендлер для добавления отслеживамого товара """
    phrase = match[0] if match else None
    if not phrase:
        msg = 'Введена пустая фраза'
    elif await user.trackeditems.filter(phrase=phrase).exists():
        msg = f'Поисковая фраза "{phrase}" уже добавлена. Попробуйте добавить другую фразу.'
    else:
        await TrackedItem.create(phrase=phrase, user=user)
        msg = f'Поисковая фраза "{phrase}" добавлена. Товары с похожей фразы будут отслеживаться.'
    await message.answer(msg)
