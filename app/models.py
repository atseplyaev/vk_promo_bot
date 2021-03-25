from tortoise.models import Model
from tortoise import fields


class Shop(Model):
    """Модель Магазина"""

    id = fields.IntField(pk=True)
    title = fields.CharField(description='Нзвание магазина', max_length=64)
    icon_url = fields.TextField(description='Ссылка на иконку')

    def __str__(self):
        return self.title


class PromoItem(Model):
    """Модель Акционного товара"""

    id = fields.IntField(pk=True)
    is_active = fields.BooleanField(description='Активный товар', default=True)
    title = fields.CharField(description='Нзвание товара', max_length=64)
    price = fields.DecimalField(description='Цена товара', decimal_places=2, max_digits=10)
    normalize_price = fields.IntField(
        description='Нормализованная цена товара (для сортировки в sqlite)'
    )
    date_start_action = fields.DateField(description='Дата начала акции')
    date_end_action = fields.DateField(description='Дата окончания акции')

    def __str__(self):
        return self.title


class User(Model):
    """Модель пользователя"""

    id = fields.IntField(pk=True)
    is_active = fields.BooleanField(description='Активный пользователь', default=True)
    vk_id = fields.CharField(description='ID пользователя из социальной сети', max_length=32)
    first_name = fields.CharField(
        description='Фамилия пользоваетля из социальной сети', max_length=32
    )
    last_name = fields.CharField(description='Имя пользоваетля из социальной сети', max_length=32)

    def __str__(self):
        return self.first_name


class TrackedItem(Model):
    """Модель отслеживаемых товаров"""

    id = fields.IntField(pk=True)
    is_active = fields.BooleanField(description='Активный товар', default=True)
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    phrase = fields.CharField(description='Фраза товара', max_length=64)

    def __str__(self):
        return self.phrase
