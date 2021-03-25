import asyncio
import os
import logging

from tortoise import Tortoise
from dotenv import load_dotenv
from vkbottle import Bot, LoopWrapper

from .blueprints import blueprints
from app import config
from .middleware import RegistrationMiddleware


logging.basicConfig(level=logging.INFO)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOTENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(DOTENV_PATH)


async def init_database() -> None:
    """
    Хендлер для открытия соединения с базой данных при старте приложения.
    """
    logging.info('Init database')
    await Tortoise.init(db_url=config.DB_URL, modules={'models': ['app.models']})


async def deinit_database() -> None:
    """
    Хендлер для закрытия соединения с базой данных при завершении приложения.
    """
    logging.info('DeInit database')
    await Tortoise.close_connections()


def setup_blueprints(bot: Bot) -> None:
    """
    Устанавливает экземпляру бота Blueprints
    """
    for blueprint in blueprints:
        blueprint.load(bot)


def create_loop_wrapper() -> LoopWrapper:
    """
    Создаёт и возвращает модифицированный LoopWrapper (цикл событий)
    """
    loop_wrapper = LoopWrapper()
    loop_wrapper.on_startup.append(init_database())
    loop_wrapper.on_shutdown.append(deinit_database())
    return loop_wrapper


def setup_middlewares(bot: Bot) -> None:
    """
    Устанавливает мидлвари экземпляру бота
    """
    bot.labeler.message_view.register_middleware(RegistrationMiddleware())


def create_bot() -> Bot:
    """
    Создаёт и возвращает экземпляр бота
    """
    loop_wrapper = create_loop_wrapper()
    bot = Bot(os.environ.get('VK_API_TOKEN'), loop_wrapper=loop_wrapper)
    setup_blueprints(bot)
    setup_middlewares(bot)
    return bot


def main():
    bot = create_bot()
    bot.run_forever()


if __name__ == '__main__':
    main()
