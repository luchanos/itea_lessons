import psycopg2
from datetime import date
from logging import getLogger, StreamHandler
import sys

# conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")


# 1 способ реализации Singletone
# class MyConnectClass:
#     cnt = 0
#     # хранить коннекты к БД в таком виде небезопасно и негибко
#
#     def __init__(self, dsn):
#         self.conn = psycopg2.connect(dsn)
#
#     def __new__(cls, *args, **kwargs):
#         if cls.cnt > 0:
#             raise Exception("Нельзя создавать больше одного экземпляра!")
#         cls.cnt += 1
#         return super().__new__(cls)

def func(par):
    a = 1
    if par == 0:
        a = a + 1


func(0)
func(1)


# 2 способ реализации Singletone
def singletone(cls):
    cnt = 0

    def inner(*args, **kwargs):
        nonlocal cnt
        if cnt > 0:
            raise ValueError("Нельзя!")
        cnt += 1
        return cls(*args, **kwargs)
    return inner


@singletone
class MyConnectClass:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)


@singletone
class TestClass:
    pass


my_connection = MyConnectClass("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
# my_connection2 = MyConnectClass("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
# test_ex = TestClass()
# test_ex2 = TestClass()

# создаём логгер
logger = getLogger(__name__)

# Уровни логирования
# DEBUG
# INFO
# WARNING
# ERROR

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

logger.setLevel("ERROR")
# logger.debug("Сообщение уровня DEBUG")
# logger.info("Сообщение уровня INFO")
# logger.warning("Сообщение уровня WARNING")
# logger.error("Сообщение уровня ERROR")




password_from_outer_request = "FREEDOM"
# password_from_outer_request = sys.argv[1]
ethalon_passwor = "FREEDOM"  # такие вещи хранят в переменных окружения либо в базе в захэшированном виде


def check_password(obj):
    def inner(*args, **kwargs):
        if password_from_outer_request == ethalon_passwor:
            return obj(*args, **kwargs)
        else:
            raise Exception("Wrong Password!")
    return inner


# @check_password
def division(a, b):
    return a / b


# @check_password
# class SomeClass:
#     def __init__(self):
#         c = 1


# class SomeClass2(SomeClass):
#     pass


# не будет работать, т.к. в SomeClass теперь лежит ФУНКЦИЯ
# d = SomeClass2()
# print(d)


# print(password_from_outer_request)
# d = SomeClass()
# print("НАЧИНАЮ РАБОТАТЬ!")
# print(f"ПРИНЯТЫЕ АРГУМЕНТЫ: {sys.argv}")
# print("ЗАКАНЧИВАЮ РАБОТАТЬ!")

# print(type(SomeClass))
# print(type(SomeClass()))

# f = division
# print(f)

# a = SomeClass
# print(a)
# print(type(a))

# c = 1
# ex = SomeClass()
# print(ex)
# c = 1
# print(division(1, 2))


@check_password
class Shop:  # модель магазина
    CREATE_SHOP_QUERY = '''INSERT INTO shops (shop_name, address, created_dt) VALUES (%s, %s, %s) RETURNING shop_id'''

    CHANGE_SHOP_NAME_QUERY = '''
    UPDATE shops SET shop_name = %s, updated_dt = %s WHERE shop_id = %s RETURNING *
    '''

    def __init__(self, shop_name, address, shop_id=None):
        self.shop_name = shop_name
        self.address = address
        self.shop_id = shop_id

    def __create_new_shop(self):
        """Записывает данные о магазине в БД"""
        cursor = my_connection.conn.cursor()
        with my_connection.conn, cursor:
            cursor.execute(self.__class__.CREATE_SHOP_QUERY, (self.shop_name, self.address, date.today()))
            self.shop_id = cursor.fetchone()[0]
            logger.info("New shop with id %d has been created" % self.shop_id)

    def change_shop_name(self, new_shop_name):
        cursor = my_connection.conn.cursor()
        with my_connection.conn, cursor:
            cursor.execute(self.__class__.CHANGE_SHOP_NAME_QUERY, (new_shop_name, date.today(), self.shop_id))
            res = cursor.fetchall()[0]  # вернем полную запись
            print(res)
            logger.info("Shop name for shop with id %d has been modified" % self.shop_id)

    def __call__(self, *args, **kwargs):
        self.__create_new_shop()


# secret_password = "some secret"
# current_password = "123"  # эта переменная будет заполняться на основании того, что нашему приложению или модулю
# # прилетит извне
# try:
#     if secret_password == current_password:
#         shop = Shop(shop_name="Березка", address="Киев")
#     else:
#         raise Exception("Wrong Password!")
# except:
#     print("Я поймал ошибку!")

# shop = Shop(shop_name="Березка", address="Киев")
# shop.__create_new_shop()
# shop()


def func_1():
    print('asfv')


def func_3():
    print('2')


def func_2():
    print('3')


func_mapper = {
    "1": func_1,
    "2": func_2,
    "3": func_3
}

# answer = input("Введите номер функции на запуск: ")
# func_mapper[answer]()
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
        # 'test': {1, 2, 3} # упадём с ошибкой!
    }
}


json_object = json.dumps(products)  # сериализовать в строку (dumpS)
# print(json_object)
# print(type(json_object))

# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(products, json_f)  # превратит данные из словаря в файл
b_str = b'{"Onion": {"price": 12, "in_stock": 1000, "description": "\u041b\u0443\u043a"}, ' \
        b'"Tomato": {"price": 4, "in_stock": 10000, "description": "\u041f\u043e\u043c\u0438\u0434\u043e\u0440\u044b"}, ' \
        b'"Cucumber": {"price": 10, "in_stock": 500, "description": "\u041e\u0433\u0443\u0440\u0446\u044b"}}'

s_str = '{"Onion": {"price": 12, "in_stock": 1000, "description": "\u041b\u0443\u043a"}, ' \
        '"Tomato": {"price": 4, "in_stock": 10000, "description": "\u041f\u043e\u043c\u0438\u0434\u043e\u0440\u044b"}, ' \
        '"Cucumber": {"price": 10, "in_stock": 500, "description": "\u041e\u0433\u0443\u0440\u0446\u044b"}}'

# with open("products_data.json", "r", encoding="UTF-8") as json_f:
#     products_dict = json.loads(b_str)  # превратит данные из строки/байт-строки в словарь
#     products_d = json.load(json_f)
#     print(products_d)
#     print(type(products_d))

# b_s = json.loads(b_str)
# print(b_s)
# print(type(b_s))

s_st = json.loads(s_str)
print(s_st)
print(type(s_st))

# Если хотим записать данные в json файл - используем dump
# Если хотим преобразовать их в строку - используем dumps
# Если хотим прочитать данные из json файла сразу в виде словаря - используем load
# Если хотим получить словарь из строки или байтовой строки - используем loads


# print(type(products_dict), products_dict)