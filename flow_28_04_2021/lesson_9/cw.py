"""
1. (ПИШЕМ КАСТОМНЫЕ КЛАССЫ) На основе прошлых ДЗ необходимо создать модели представлений для классов
ДЕПАРТАМЕНТЫ (Departments), СОТРУДНИКИ (Employees), ЗАЯВКИ (Orders). Реализовать магические методы вывода
информации на экран как для пользователя, так и для "машинного" отображения.

Предусмотреть все необходимые ограничения и связи моделей между собой (*).

У каждой модели предусмотрите метод, который бы мог осуществлять запись хранимой в экземпляре информации в отдельный
json-файл с именем вида <id записи>.json. Если id не существует - выдавать ошибку.

2. Преобразовать все самописные классы-модели из прошлых ДЗ (из задачи 1: Заявки - Orders, Департаменты - Departments,
Сотрудники - Employees) в модели для использования в MongoDB. Предусмотреть необходимые связи, валидацию
данных и ограничения.

Написать функции, которые будут:

создавать/изменять/удалять новую заявку/сотрудника/департамент

Подсказка: у вас должно получиться 3 модели и 9 функций =)
"""

# MongoDB - нереляционная база данных. Хранит данные по сути в виде json.
# Прекрасно заходит под небольшие проекты. Отличается высокой скоростью работы - на чтение и запись.

# Джойнить можно, но сложно! Потому что по сути мы джойним не таблицы, а отдельные документы.
# Джойны в курсе не рассматриваются.

# Пример агрегационного запроса к MongoDB:

"""
Model._get_collection().aggregate([
    { '$group' : 
        { '_id' : { 'carrier' : '$carrierA', 'category' : '$category' }, 
          'count' : { '$sum' : 1 }
        }
    }
])
"""

# Не самый дружелюбный синтаксис. не правда ли?

# чтобы не писать сырой код для взаимодействия с БД люди придумали такую вещь, как ORM - Object Relation Mapping.
# Они существуют для каждой популярной БД и заменяют собой необходимость писать сырые запросы и прокидывать их напрямую.

# Обычно модели хранят в файле models.py
# для MongoDB используется библиотека mongoengine
import mongoengine as me
from datetime import datetime as dt

me.connect("LESSON_8_DB")  # если такой БД нет, то она будет создана автоматически


# нет понятия таблица, вместо неё понятие коллекция
class UserProfile(me.Document):
    login = me.StringField(required=True, min_length=3, max_length=120, unique=True)
    password = me.StringField(required=True, min_length=2)  # в таком виде хранить пароли не стоит, надо хэшировать
    about_me = me.StringField()
    likes = me.IntField(default=0)


class User(me.Document):
    # объявляем поля коллекций
    first_name = me.StringField(min_length=1, max_length=100, required=True)
    last_name = me.StringField(min_length=1, max_length=100)
    interests = me.ListField()
    age = me.IntField(min_value=12, max_value=99)
    created_at = me.DateTimeField()
    user_profile = me.ReferenceField(UserProfile, reverse_delete_rule=me.CASCADE)

    # CASCADE - удалит юзера при удалении профайла
    # подробнее - https://docs.mongoengine.org/apireference.html

    def say_hello(self):
        return f"Hello, {self.first_name}"

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.interests}, {self.age}"

    def save(self, *args, **kwargs):
        self.created_at = dt.now()
        return super().save(*args, **kwargs)


class Products(me.Document):
    name = me.StringField()
    price = me.IntField()
    in_stock = me.IntField()
    description = me.StringField()

    def __str__(self):
        return f"{self.name}, {self.price}, {self.in_stock}, {self.description}"

    # def __repr__(self):
    #     return "Машинный вывод объекта"


# создаём объект продукта
product_1 = Products(name="Onion", price=100, in_stock=1000, description="Лук-лучок")

# пока он не записан в базу!!! для сохранения надо вызвать .save()
res = product_1.save()
print(res.id)  # имеем доступ к id

# а теперь можно пойти в Compass и посмотреть что там теперь лежит. Айдишник будет присвоен автоматически.

# by_id = Products.objects.get(id="60b24f643befbaa8dcac5fb1")
# print(by_id)

# Теперь попробуем прочитать все данные из БД:
# data_from_mong_products = Products.objects()
# for obj in data_from_mong_products:
#     print(obj)
#     # можно сразу перегонять в json
#     js_data = obj.to_json()
#     print(type(js_data), js_data)
#     # и получать словарь при желании
#     dict_data = json.loads(obj.to_json())
#     print(type(dict_data), dict_data)

# print(data_from_mong_products)

# res = Products.objects(name="Onion")
# res_1 = Products.objects(name__ne="Onion")
# res_2 = Products.objects(in_stock__gt=50)

# .count() - вернёт количество записей в выборке

# ne - не равно
# lt - меньше, чем
# lte - меньше, чем или равно
# gt - больше, чем
# gte - больше или равно
# in - проверка на вхождение
# nin - проверка на невхождение

# mongod --dbpath Users/data - так я поднимал базу на своём компе (macOS)
# Compass - интерфейс для работы с БД по типу DBeaver, только для Mongo

# СОЗДАЁМ ТЕСТОВЫЙ НАБОР ДАННЫХ:

user_profiles_list = [
    {"login": "lol",
     "password": "123",
     "about_me": "some lol",
     "likes": 3},
    {"login": "kek",
     "password": "1234",
     "about_me": "some kek",
     "likes": 5},
    {"login": "cheburek",
     "password": "12345",
     "about_me": "some cheburek",
     "likes": 6},
    {"login": "some_user",
     "password": "1234567",
     "about_me": "some some_user",
     "likes": 0}
]


user_data_list = [
    {"first_name": "Nikolai",
     "last_name": "Sviridov",
     "interests": ["mma", "programming", "blogging"],
     "age": 29
     },
    {"first_name": "Anna",
     "last_name": "Prozorova",
     "interests": ["smimming", "dancing", "singing"],
     "age": 35
     },
    {"first_name": "Semen",
     "last_name": "Ivanov",
     "interests": ["fishing", "riding"],
     "age": 21
     },
    {"first_name": "Chubaka",
     "last_name": "Chubakov",
     "interests": ["barking"],
     "age": 99
     }
]

# first_name = me.StringField(min_length=1, max_length=100, required=True)
# last_name = me.StringField(min_length=1, max_length=100)
# interests = me.ListField()
# age = me.IntField(min_value=12, max_value=99)
# created_at = me.DateTimeField()

# удалить все записи из коллекций:
User.objects.all().delete()
UserProfile.objects.all().delete()

# записываем тестовые данные в БД
for user_profile_data in zip(user_profiles_list, user_data_list):
    user_profile = UserProfile(**user_profile_data[0]).save()
    user = User(user_profile=user_profile, **user_profile_data[1]).save()


# вариант комбинированной выборки:
users = User.objects((me.Q(age__in=[35, 29]) | me.Q(last_name="Chubakov")))
print(users)
users = User.objects((me.Q(age=99) & me.Q(last_name="Chubakov")))
print(users)


# правило удаления записей, которые соединены с данной записью (правило обратного удаления)
# user_profile = me.ReferenceField(UserProfile, reverse_delete_rule=me.CASCADE) # каскадное
# user_profile = me.ReferenceField(UserProfile, reverse_delete_rule=me.NULLIFY)  # занулить

# КОМАНДЫ ДЛЯ КОНСОЛИ COMPASS:

# use <имя базы данных> - выбираем БД, с которой хотим осуществлять работу.
# db - проверить, с какой БД сейчас работаем
# show dbs - список всех БД

# Если мы создали новую БД, но там пока не лежит ни одного документа, то она не будет отображаться в списке.
# Она появится в нём только когда туда что-то попадёт. По факту нам даже не нужно создавать эту БД, просто пишем
# куда мы хотим вставить документ - БД создастся сама собой!
