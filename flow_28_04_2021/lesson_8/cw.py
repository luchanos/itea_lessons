"""
1. Напишите декоратор для класса, который бы при создании экземпляра этого класса осуществлял бы запись информации об
этом в текстовый файл. Пример записи: 2012-01-01 15:04 Создан экземпляр класса TestClass по адресу памяти x01223342

2. На основе прошлых ДЗ необходимо создать модели представлений для классов ДЕПАРТАМЕНТЫ (Departments),
СОТРУДНИКИ (Employees), ЗАЯВКИ (Orders). Реализовать магические методы вывода информации на экран как для пользователя,
так и для "машинного" отображения.

Предусмотреть все необходимые ограничения и связи моделей между собой.

У каждой модели предусмотрите метод, который бы мог осуществлять запись хранимой в экземпляре информации в отдельный
json-файл с именем вида <id записи>.json. Если id не существует - выдавать ошибку.
"""

# json - замечательный формат данных, напоминающий словарь
# Один из наиболее распространённых форматов, используемых в web, наряду с XML
# пример ответа "ручки" сайта Авито, которая располагается в свободном доступе и отдаёт json в составе своего ответа:
# https://www.avito.ru/js/v1/side_block?locationId=653240&showWaitRating=true
# json позволяет web приложениям общаться между собой.

# получим вот такой результат:
"""
{
  "recentlyViewed": {
    "hash": "p47rxtx97qscs8484s84ook0ocs00wk",
    "engine": "recently_viewed",
    "position": 1
  },
  "navbar": {
    "hash": "jcaa8qr457cc8800gg8c0ss8s4scwo0",
    "shouldShowOfferLink": false
  },
  "servicesInfo": {
    "hash": "1o2sgt0561s080kcckog0cwkgs04kso"
  }
}
"""

# Для работы с документами подобного вида в Python предусмотрен модуль json:

import json


products = {
    'Onion': {
        'price': 12,
        'in_stock': 1000,
        'description': 'Лук'
    },
    'Tomato': {
        'price': 4,
        'in_stock': 10000,
        'description': 'Помидоры'
    },
    'Cucumber': {
        'price': 10,
        'in_stock': 500,
        'description': 'Огурцы',
        # 'test': {1, 2, 3}
    }
}

# предположим, что на стороне нашего прекрасного Питонячьего сервиса мы сформировали словарь и ли список и хотим
# хранить его на диске или передавать его в виде json по сети. Сначала нужно привести наши данные в пригодный для этого
# вид:

# сериализация - процесс перегонки питоновских данных в НЕпитоновские
# json_object = json.dumps(products)  # сериализовать в строку (dumpS)
# print(json_object)
# print(type(json_object))  # это класс СТРОКА!

# как мы уже говорили ранее эту строку можно преобразовать в байты и отправить, скажем, по сети)

# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(products, json_f)  # превратит данные из словаря в файл

# encoding - это параметр кодировки. Их бывает великое множество, они отвечают за правила, по которым машина будет
# читать данные из файла. Помните ситуацию, когда вы открываете файл, а там крокозябры? Всё дело в том, что кодировка,
# в которой он был записан и кодировка, в которой файл читается - не совпадают, поэтому лучше задавать её всегда явно.
# Кодировка по умолчанию может быть своя в каждой системе (настраивается): UTF-8 (Mac), cp-1251 (Windows).

# Кортеж и множество - не сериализуется, они будут преобразованы в список, если находятся в составе сериализуемой
# структуры

l1 = [1, 2, 3]
t1 = (1, 2, 3)  # будет преобразовано в список
s1 = {1, 2, 3}  # не будет сериализовано - вылезет ошибка

# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(s1, json_f)  # превратит данные из словаря в файл

# Обратный процесс - десериализация. Когда мы получили json-данные и теперь надо превратить их во что-то, с чем
# можно было бы работать в виде хорошо знакомых питоновских типов данных
# with open("products_data.json", "r", encoding="UTF-8") as json_f:
#     products_dict = json.load(json_f)  # превратит данные из файла в словарь

# print(products_dict, type(products_dict))

# допустим нам прилетела по сети строка

b_str = b'{"Onion": {"price": 12, "in_stock": 1000, "description": "\u041b\u0443\u043a"}, ' \
        b'"Tomato": {"price": 4, "in_stock": 10000, "description": "\u041f\u043e\u043c\u0438\u0434\u043e\u0440\u044b"}, ' \
        b'"Cucumber": {"price": 10, "in_stock": 500, "description": "\u041e\u0433\u0443\u0440\u0446\u044b"}}'

# или

s_str = b'{"Onion": {"price": 12, "in_stock": 1000, "description": "\u041b\u0443\u043a"}, ' \
        b'"Tomato": {"price": 4, "in_stock": 10000, "description": "\u041f\u043e\u043c\u0438\u0434\u043e\u0440\u044b"}, ' \
        b'"Cucumber": {"price": 10, "in_stock": 500, "description": "\u041e\u0433\u0443\u0440\u0446\u044b"}}'
# with open("products_data.json", "r", encoding="UTF-8") as json_f:
#     products_dict = json.loads(b_str)  # превратит данные из строки/байт-строки в словарь
# print(type(products_dict), products_dict)

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
    password = me.StringField(required=True, min_length=8)  # в таком виде хранить пароли не стоит, надо хэшировать
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
        super().save(*args, **kwargs)


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

# КОМАНДЫ ДЛЯ КОНСОЛИ COMPASS:

# use <имя базы данных> - выбираем БД, с которой хотим осуществлять работу.
# db - проверить, с какой БД сейчас работаем
# show dbs - список всех БД

# Если мы создали новую БД, но там пока не лежит ни одного документа, то она не будет отображаться в списке.
# Она появится в нём только когда туда что-то попадёт. По факту нам даже не нужно создавать эту БД, просто пишем
# куда мы хотим вставить документ - БД создастся сама собой!
