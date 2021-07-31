import psycopg2
from sys import argv
from envparse import Env

"""задача про argv с флагами"""

env = Env()

DB_URL = env.str("DB_URL", default='postgresql://newuser:qwerty@localhost:5432/postgres')

# print(argv)
# DB_URL = "postgresql://newuser:qwerty@localhost:5432/postgres"
# DB_URL = argv[1]

SELECT_QUERY = """SELECT * FROM products p WHERE description = '%s'"""
INSERT_QUERY = """INSERT INTO products (description, quantity) VALUES ('%s', %d);"""

conn = psycopg2.connect(DB_URL)
with conn.cursor() as cursor:
    cursor.execute(SELECT_QUERY % 'Лук')
    cursor.execute(INSERT_QUERY % ('Товар 1', 100))
    conn.commit()
    # print(cursor.fetchmany(4))
    # print(cursor.fetchone())
    # print(cursor.fetchone())
    # print(cursor.fetchone())
    # print(cursor.fetchone())
    # data = cursor.fetchall()
    # print(data)

"""Не забыть рассказать про генераторы, envparse -> env, argv, миграции"""

# для создания новой миграции - yoyo new trading_db/ -m "table for shops"
# для прогона миграций - yoyo apply trading_db/ --database postgres://postgres:dbpass@0.0.0.0:5432/postgres
# откат миграций - yoyo rollback trading_db/ --database postgres://postgres:dbpass@0.0.0.0:5432/postgres
