"""ДЗ

Вспомним класс, который мы реализовывали в рамках ДЗ №2 (класс Заявка - Order).  Нужно взять его за основу и теперь
реализовать конкретные методы, которые будут получать заявку из БД

 - метод, который будет получать заявку из БД по её id и на основе полученных данных собирать объект класса Order."""

import psycopg2
from datetime import date
from logging import getLogger, StreamHandler
import sys

# создаём логгер
logger = getLogger(__name__)
logger.setLevel("INFO")
stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)


def singletone(cls):
    cnt = 0

    def inner(*args, **kwargs):
        nonlocal cnt
        if cnt == 1:
            raise ValueError("Нельзя!")
        cnt += 1
        return cls(*args, **kwargs)
    return inner


@singletone  # может существовать только один экземпляр
class Connect:
    # хранить коннекты к БД в таком виде небезопасно и негибко
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)


connect = Connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
connect_2 = Connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")


# Выход есть! Заводим переменную окружения!
from envparse import Env

env = Env()

# теперь значение будет подтягиваться из переменной окружения
DB_URL = env.str("DB_URL")
print(DB_URL)

BIG_BOSS_TOKEN_SERVICE = env.str("BIG_BOSS_TOKEN_SERVICE", default="big_boss_service_token")
ADMIN_SERVICE_TOKEN = env.str("ADMIN_SERVICE_TOKEN", default="admin_service_token")
USER_SERVICE_TOKEN = env.str("USER_SERVICE_TOKEN", default="user_service_token")

SECRET_SHOP_TOKEN_LIST = [BIG_BOSS_TOKEN_SERVICE, ADMIN_SERVICE_TOKEN]

# можно задать её с дефолтными значениями
# DB_URL = env.str("DB_URL", default="postgres://postgres:dbpass@0.0.0.0:5432/postgres")

# миграции можно накатывать с помощью yoyo-migrations

CREATE_SHOP_TABLE = """
CREATE TABLE shops (
shop_id SERIAL NOT NULL,
shop_name TEXT NOT NULL,
address TEXT NOT NULL,
created_dt DATE NOT NULL,
updated_dt DATE
)
"""


class PasswordException(Exception):
    def __init__(self, message):
        self.message = message


# допустим, что инициатором наших изменений является запрос по сети и мы хотим ограничить его доступы к некоторым
# частям нашего проекта. Можно использовать токены + декоратор для класса или функций
def password_checker(service_token):
    def outer(cls):
        def inner(*args, **kwargs):
            if service_token in SECRET_SHOP_TOKEN_LIST:  # или можно просто внаглую запрашивать пароль на экране
                return cls(*args, **kwargs)
            logger.warning("Wrong password")
            raise PasswordException("Wrong password: %s" % service_token)
        return inner
    return outer


# @password_checker(service_token="MY_TOKEN") # неправильный ввод пароля, доступ к созданию экземпляров ЗАКРЫТ
@password_checker(service_token="big_boss_service_token")  # правильный ввод пароля
class Shop:
    CREATE_SHOP_QUERY = '''INSERT INTO shops (shop_name, address, created_dt) VALUES (%s, %s, %s) RETURNING shop_id'''

    CHANGE_SHOP_NAME_QUERY = '''
    UPDATE shops SET shop_name = %s, updated_dt = %s WHERE shop_id = %s RETURNING *
    '''

    def __init__(self, shop_name, address, shop_id=None):
        self.shop_name = shop_name
        self.address = address
        self.shop_id = shop_id

    def create_new_shop(self):
        """Записывает данные о магазине в БД"""
        cursor = connect.conn.cursor()
        with connect.conn, cursor:
            cursor.execute(self.__class__.CREATE_SHOP_QUERY, (self.shop_name, self.address, date.today()))
            self.shop_id = cursor.fetchone()[0]
            logger.info("New shop with id %d has been created" % self.shop_id)

    def change_shop_name(self, new_shop_name):
        cursor = connect.conn.cursor()
        with connect.conn, cursor:
            cursor.execute(self.__class__.CHANGE_SHOP_NAME_QUERY, (new_shop_name, date.today(), self.shop_id))
            res = cursor.fetchall()[0]  # вернем полную запись
            print(res)
            logger.info("Shop name for shop with id %d has been modified" % self.shop_id)

    def __call__(self, *args, **kwargs):
        self.create_new_shop()


def main():
    print("ПРОГРАММА УПРАВЛЕНИЯ МАГАЗИНАМИ BY LUCHANOS CORPORATION")
    with connect.conn:
        while True:
            user_choice = input("""
            Введите желаемое действие:
            1. Работа с продуктами
            2. Работа с магазинами
            3. Работа с департаментами
            """)
            if user_choice.lower() == "Q":
                break

            # очень негибкая конструкция, надо порефачить - можно перевести всё на словари
            if user_choice == "1":
                user_choice = input("""Введите желаемое действие:
                1. Добавление продукта
                2. Изменение продукта
                3. Удаление продукта
                """)
            elif user_choice == "2":
                user_choice = input("""Введите желаемое действие:
                1. Добавление магазина
                2. Изменение информации о магазине
                3. Удаление магазина
                """)
                if user_choice == "1":
                    shop_name = input("Введите имя магазина: ")
                    shop_address = input("Введите адрес магазина: ")
                    shop = Shop(shop_name=shop_name, address=shop_address)
                    shop()  # записываем магазин в базу
            elif user_choice == "3":
                user_choice = input("""Введите желаемое действие:
                1. Добавление департамента
                2. Изменение департамента
                3. Удаление департамента
                """)
            else:
                print("Невалидный ввод! Повторите или введите Q/q для выхода.")


if __name__ == "__main__":
    # main()
    # shop = Shop(shop_name="Березка", address="Москва")
    # shop()
    # shop_2 = Shop(shop_name="Елисеевский", address="Санк-Петербург")
    # shop_2()
    shop_3 = Shop(shop_name="Магнит", address="Уфа")
    shop_3()
    shop_3.change_shop_name("AHAHAHAHAH")
