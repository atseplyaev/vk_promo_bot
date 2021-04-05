from vkbottle.bot import Blueprint, Message, BotLabeler
from vkbottle_types.objects import UsersUser

from vkbottle import Callback, GroupEventType, GroupTypes, Keyboard, Text
from app.models import User
from app.services import get_main_keyboards

bp = Blueprint()


# KEYBOARD = (
#     Keyboard(one_time=False, inline=True)
#     .add(Callback('Пришли мне привет', payload={'cmd': 'register_1'}))
#     .get_json()
# )

# KEYBOARD = (
#     Keyboard(one_time=True).add(Text('Зарегистрироваться', payload={'command': 'start'})).get_json()
# )


# @bp.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
# async def handle_message_event(event: GroupTypes.MessageEvent):
#     # event_data parameter accepts three object types
#     # "show_snackbar" type
#     print(event.object.payload)
#     event.object.
#     await bp.api.messages.send_message_event_answer(
#         event_id=event.object.event_id,
#         user_id=event.object.user_id,
#         peer_id=event.object.peer_id,
#         event_data='{"type":"show_snackbar", "text":"Сейчас я исчезну"}',
#     )


@bp.on.message(text=['Меню'])
async def menu_handler(message: Message, user: User, user_info: UsersUser):
    await message.answer('Меню', keyboard=get_main_keyboards(user))


@bp.on.message(text=['привет<!>', 'hi'])
async def hi_handler(message: Message, user: User, user_info: UsersUser):
    await message.answer(f'Привет, {user_info.first_name}!', keyboard=get_main_keyboards(user))


@bp.on.private_message(text='/register_1')
async def callback_hi_handler(message: Message, user: User, user_info: UsersUser):
    await message.answer(f'Callback Привет {user_info.first_name}!')
