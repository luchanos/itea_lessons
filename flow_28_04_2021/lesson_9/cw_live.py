# NoSQL БД

# Типовой документ:
d = {
    'id': 1,
    'price': 12,
    'in_stock': 1000,
    'description': 'Лук',
}

# Прочитать про хэш-таблицы 5 глава Грокаем Алгоритмы
# [] () {}
# [_____________________]
# f(key) = (key * 100 + 5) / 4  # пример плохой (наверное) хэш-функции
# подсчитанное значение называется ХЭШ
# сущность для хранения информации в NoSQL базах - это коллекции или их аналоги
d['expiry_date'] = '2021-01-07'


import mongoengine as me
from datetime import datetime as dt
import json

# если в базе пока ничего не лежит, то и в интерфейсе она не будет отображаться
me.connect("LESSON_9_DB")  # если такой БД нет, то она будет создана автоматически


# такой класс называется МОДЕЛЬЮ
class UserProfile(me.Document):
    login = me.StringField(required=True, min_length=3, max_length=20)
    password = me.StringField(required=True)
    likes = me.IntField(default=0)
    about_me = me.StringField()
    created_at = me.DateTimeField()

    def __str__(self):
        return f"login: {self.login} | password: {self.password}"

    def __repr__(self):
        return f"Машинный вывод информации: login: {self.login} | password: {self.password}"

    def save(self, *args, **kwargs):
        self.created_at = dt.now()
        return super().save(*args, **kwargs)


class User(me.Document):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    age = me.IntField()
    interests = me.ListField(default=[])
    user_profile = me.ReferenceField(UserProfile, required=True)

    def __str__(self):
        return f"{self.pk} {self.first_name}"



# first_profile = UserProfile(login='Chupakabra', password='12345')
# first_profile.save()
# first_profile = UserProfile(login='Kamikadze', password='123456')
# first_profile.save()  # осуществляет запись в базу
# first_profile = UserProfile(login='Nikolai', password='123456')
# first_profile.save()  # осуществляет запись в базу


# res = UserProfile.objects.all()
# for item in res:
#     print(item)
#     js_data = item.to_json()
#     print(js_data, type(js_data))
#     # и получать словарь при желании
#     dict_data = json.loads(item.to_json())
#     print(dict_data, type(dict_data))

# res = UserProfile.objects.get(pk="60b7bfa8a057a4ee4bc6ad40")
# print(UserProfile.objects(login="Nikolai"))

# User(name="Nikolai", surname="Sviridov", interests=["programming", "teaching", "blogging", "mma"]).save()

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

UserProfile.objects.all().delete()
User.objects.all().delete()

# записываем тестовые данные в БД
for user_profile_data in zip(user_profiles_list, user_data_list):
    print(user_profile_data)
    from time import sleep
    sleep(.5)
    user_profile = UserProfile(**user_profile_data[0]).save()
    user = User(user_profile=user_profile, **user_profile_data[1]).save()


# user = User.objects.get(id='60b7d16f388a6b576e68ef22')
# user.interests = ["fishing"]
# user.save()


def some_func(a, b, c, **kwargs):
    print(a, b, c)


# some_func(1, 2)
# some_func(b=1, a=2)

# t = (1, 2, 3, 4, 5)
# d = {'a': 1, 'b': 2, 'c': 3, 'd': 4545}

# some_func(*t)
# some_func(**d)

# l = [1, 2, 3, 4]
# l_str = ['a', 'b', 'c', 'd']
# [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']]
# print(list(zip(l, l_str)))

# res = User.objects(first_name__ne="Nikolai")
# print(res)
# res_1 = UserProfile.objects(name__ne="Onion")

# .count() - вернёт количество записей в выборке

# ne - не равно
# lt - меньше, чем
# lte - меньше, чем или равно
# gt - больше, чем
# gte - больше или равно
# in - проверка на вхождение
# nin - проверка на невхождение
