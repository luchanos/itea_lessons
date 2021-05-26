import psycopg2

from envparse import Env
from datetime import date

env = Env()

# connect_str = "postgres://postgres:dbpass@0.0.0.0:5432/postgres"  # postgres://имя_юзера:пароль_для_коннекта@хост:порт
DB_URL = env.str("SOME_DB_URL", default="postgres://postgres:dbpass@0.0.0.0:5432/postgres")
print(DB_URL)

connect = psycopg2.connect(DB_URL)


from abc import ABC, abstractmethod

CREATE_SHOP_QUERY = '''INSERT INTO shops (shop_name, address, created_dt) VALUES (%s, %s, %s) RETURNING shop_id'''


class BaseModel(ABC):
    @abstractmethod
    def create_new_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete_data_by_id(self, *args, **kwargs):
        pass

    def real_method(self):
        print("Это реализованный метод")


class DataRequiredException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        self.args = args
        self.kwargs = kwargs


class Shop(BaseModel):
    CREATE_SHOP_QUERY = """INSERT INTO shops (shop_name, address, created_dt) VALUES (%s, %s, %s) RETURNING shop_id"""
    DELETE_SHOP_QUERY = """DELETE FROM shops WHERE shop_id = %s"""
    CHANGE_NAME_QUERY = """UPDATE shops SET shop_name = %s, updated_dt = %s WHERE shop_id = %s"""

    def __init__(self, shop_name=None, address=None, shop_id=None):
        self.shop_name = shop_name
        self.address = address
        self.shop_id = shop_id

    def create_new_data(self):
        with connect, connect.cursor() as cursor:
            cursor.execute(self.__class__.CREATE_SHOP_QUERY, (self.shop_name, self.address, date.today()))
            shop_id = cursor.fetchone()[0]
            self.shop_id = shop_id
        return {"shop_id": shop_id}

    def delete_data_by_id(self):
        if not self.shop_id:
            raise DataRequiredException(message="Shop_id param is required for deleting!")
        with connect, connect.cursor() as cursor:
            cursor.execute(self.__class__.DELETE_SHOP_QUERY, (self.shop_id, ))

    def change_name(self, new_name):
        with connect, connect.cursor() as cursor:
            cursor.execute(self.__class__.CHANGE_NAME_QUERY, (new_name, date.today(), self.shop_id, ))


class Departents(BaseModel):
    CREATE_SHOP_QUERY = """INSERT INTO departments (department_name) VALUES (%s) RETURNING shop_id"""
    DELETE_SHOP_QUERY = """DELETE FROM departments WHERE department_id = %s"""
    CHANGE_NAME_QUERY = """UPDATE departments SET department_name = %s, updated_dt = %s WHERE department_id = %s"""

    def __init__(self, department_name=None, department_id=None):
        self.shop_name = department_name


shop_1 = Shop(shop_name="Берёзка", address="Киев")
print(shop_1.create_new_data())
shop_1.change_name("Дуб")
