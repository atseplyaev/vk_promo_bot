from tortoise import Tortoise, run_async
from app import config


async def init():
    conf = {'models': ['app.models']}
    print(conf)
    await Tortoise.init(
        db_url=config.DB_URL,
        modules=conf
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init())
