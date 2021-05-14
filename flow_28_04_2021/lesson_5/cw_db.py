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
res = cursor.execute("""SELECT * FROM shops""")
# data = cursor.fetchall()
# data = cursor.fetchone()
data = cursor.fetchmany(2)
print(data)
