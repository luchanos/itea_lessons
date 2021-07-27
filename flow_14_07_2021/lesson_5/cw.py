from sqlalchemy import create_engine, text
engine = create_engine(url="postgresql://newuser:qwerty@localhost:5432/postgres", echo=True, future=True)


PRODUCTS_DB_CREATION = """
CREATE TABLE IF NOT EXISTS products (
product_id SERIAL PRIMARY KEY,
description TEXT NOT NULL,
quantity INTEGER NOT NULL
)
"""

# простой коннект к БД:
with engine.connect() as conn:
    result = conn.execute(text(PRODUCTS_DB_CREATION))  # после запуска будет выведено сообщение в лог
    conn.commit()  # фиксируем наши изменения, после чего у нас появится таблица в нашей базе


# тестовые данные для магазина
TEST_PRODUCTS_CREATION = [
    ("Лук", 100),
    ("Чеснок", 200),
    ("Картошка", 300),
    ("Молоко", 400)
]

# запрос для вставки тестовых данных. Вместо %s можно использовать знаки вопроса (?).
PRODUCT_INSERTION_SCRIPT = """
INSERT INTO products (description, quantity) VALUES ('%s', %s);
"""

#  вставка тестовых данных
# with engine.connect() as conn:
#     for product_tuple in TEST_PRODUCTS_CREATION:
#         conn.execute(text(PRODUCT_INSERTION_SCRIPT % product_tuple))
#     conn.commit()

SELECT_QUERY = """SELECT * FROM products"""

with engine.connect() as conn:
    result = conn.execute(text(SELECT_QUERY))
    print(result.all())
