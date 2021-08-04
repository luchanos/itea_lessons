from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, registry

DB_URL = "postgresql://newuser:qwerty@localhost:5432/postgres"


engine = create_engine(url=DB_URL, echo=True, future=True)


PRODUCTS_DB_CREATION = """
CREATE TABLE IF NOT EXISTS products (
product_id SERIAL PRIMARY KEY,
description TEXT NOT NULL,
quantity INTEGER NOT NULL
)
"""

# простой коннект к БД:
# with engine.connect() as conn:
#     result = conn.execute(text(PRODUCTS_DB_CREATION))  # после запуска будет выведено сообщение в лог
#     conn.commit()  # фиксируем наши изменения, после чего у нас появится таблица в нашей базе


# тестовые данные для магазина
# TEST_PRODUCTS_CREATION = [
#     ("Лук", 100),
#     ("Чеснок", 200),
#     ("Картошка", 300),
#     ("Молоко", 400)
# ]

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

# получение результата селекта из базы
# with engine.connect() as conn:
#     result = conn.execute(text(SELECT_QUERY))
#     print(result.all())

metadata = MetaData()
user_table = Table("user_account",
                   metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(30)),
                   Column('fullname', String))

address_table = Table(
    "address",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

# надо сделать привязку метадаты к БД
# metadata.bind = engine
# metadata.create_all()


##############
Base = declarative_base()


# альтернативное написание:
class User(Base):
    __tablename__ = 'user_account_ORM'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address_ORM'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account_ORM.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


sandy = User(name="sandy", fullname="Sandy Cheeks")
Base.metadata.create_all(engine)
