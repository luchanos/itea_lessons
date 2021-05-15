import sqlite3
from datetime import datetime
# с помощью этой волшебной библиотеки можно взаимодействовать с файлами sqlite3 db

INSERT_DATA = """
INSERT INTO shops (description, address, product_id) 
VALUES ('магазин Продукты', 'г.Москва, ул. Пушкина, д.2', 123)
"""

conn = sqlite3.connect("itea_db.db")  # создаём соединение
cursor = conn.cursor()  # создаём курсор - специальную сущность, которая будет запускать наши запросы к базе

# res = cursor.execute("""SELECT * FROM shops""")
# for row in res:
#     print(row)

# cursor.execute(INSERT_DATA)
# conn.commit()  # не забываем сделать коммит нашей записи, если не используем менеджер контекста

# Можно прокинуть параметризованный запрос
INSERT_DATA_PARAMETRIZED = """
INSERT INTO shops (description, address, product_id) 
VALUES ($1, $2, $3)
"""

description = "ГУМ"
address = "г.Москва, Красная площадь, д.2"
product_id = 123

# with conn:
#     cursor.execute(INSERT_DATA_PARAMETRIZED, (description, address, product_id))

# Добавляем дату создания записи в базе:
INSERT_DATA_PARAMETRIZED_WITH_DATA = """
INSERT INTO shops (description, address, product_id, created_dt) 
VALUES ($1, $2, $3, $4)
"""

# with conn:
#     cursor.execute(INSERT_DATA_PARAMETRIZED_WITH_DATA,
#                    (description, address, product_id, datetime.now()))
    # дата автоматически будет преобразована к текстовому формату

# res = cursor.execute("""SELECT * FROM shops""")
# for row in res:
#     for row_data in row:
#         print(type(row_data), row_data)  # данные возвращаются уже в питонопригодном формате


# извлекает следующую строку из результирующего набора
# fetchone - вернет очередное значение из результирующего набора
# fetchall - вернет все данные из результирующего набора
# fetchmany - вернет столько значений, сколько укажем в параметре
# res = cursor.execute("""SELECT * FROM shops""")
# data = cursor.fetchall()
# data = cursor.fetchone()
# data = cursor.fetchmany(2)
# print(data)


# для PostgreSQL существует библиотека psycopg2
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")

# принцип работы такое же, как и с библиотекой sqlite3

product_data = [("Репчатый лук от отечественного производителя", 100, "Лук репчатый"),
                ("Капуста белокочанная высшего сорта", 200, "Капуста"),
                ("Картофель молодой", 300, "Картофель"),
                ("Свекла сахарная импортная", 50, "Свекла сахарная"),
                ("Яйцо куриные высшей категории", 70, "Яйцо куриное")]

SELECT_QUERY = """SELECT * FROM products"""

# получаем данные из БД
with conn.cursor() as cursor:
    cursor.execute(SELECT_QUERY)
    print(cursor.fetchall())

# записываем данные в БД
# sql.SQL - это обёртка вокруг строки для того, чтобы можно было без проблем прокидывать параметризованные запросы
INSERT_QUERY = sql.SQL("""INSERT INTO products (description, quantity, product_name) VALUES (%s, %s, %s)""")

# два контекстных менеджера
with conn:
    with conn.cursor() as cursor:
        for product in product_data:
            cursor.execute(INSERT_QUERY, product)

# можно свести в один:
with conn, conn.cursor() as cursor:
    for product in product_data:
        cursor.execute(INSERT_QUERY, product)

# подробнее вот тут - https://www.psycopg.org/docs/sql.html
