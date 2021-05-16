"""SQL и базы данных

Создать базу данных с названием order_service_db. Создать в ней несколько таблиц:

Таблица ЗАЯВКИ (orders)
- id заявки (order_id) - целое число
- дата создания (created_dt) - текст
- дата обновления заявки (updated_dt) - текст
- тип заявки (order_type) - текст
- описание (description) - текст
- статус заявки (status) - текст
- серийный номер аппарата (serial_no) - целое число
- id создателя заявки (creator_id) - целое число

Таблица СОТРУДНИКИ (employees)
- id сотрудника (employee_id) - целое число
- ФИО (fio) - текст
- должность (position) - должность
- id подразделения (department_id) - целое число

Таблица ПОДРАЗДЕЛЕНИЯ (departments)
- id подразделения (department_id) - целое число
- название подразделения (department_name) - текст

Написать код создания таблиц на языке SQL, предусмотреть необходимые ограничения.
"""

# ЧТО ТАКОЕ БАЗА ДАННЫХ?
# Простым языком, база данных это структурированное хранилище информации. В зависимости от структуры
# построения баз данных они могут быть (неполный список):
# - реляционные (Postgresql, SQLite)
# - документоориентированные (MongoDB)
# - time-series (InfluxDB)

# В реляционных базах данных вся информация хранится в виде таблиц, которые могут быть связанны между собой.


# SQL - SQL — простыми словами, это язык программирования структурированных запросов
# (SQL, Structured Query Language), который используется в качестве способа общения с базами данных.

# SQLite - самая легковесная БД, её структура умещается в файл, который можно перекидывать хоть
# по сети или в телеграмме или по почте.

# БАЗОВЫЕ КОМАНДЫ:
# СОЗДАНИЕ БАЗЫ ДАННЫХ SQLite3 - создаём через SQLite Studio, через кнопку new database, где указываем путь к файлу

# СОЗДАНИЕ ПРОСТОЙ ТАБЛИЦЫ:
"""CREATE TABLE products (
    product_id INTEGER,
    description TEXT,
    quantity INTEGER
    );
"""

# ХОЗЯЙКЕ НА ЗАМЕТКУ: id - плохое имя для колонки, лучше выбирать другое имя, например product_id

# Если попытаться повторно создать ту же самую таблицу, то вылезет ошибка. Бывают ситуации, например когда
# нужно повторно прогнать миграции в базе.(это набор команд, которые выстраивают структуру базы) и тогда
# полезно добавлять проверку на существование таблицы:

# СОЗДАНИЕ ПРОСТОЙ ТАБЛИЦЫ С ПРОВЕРКОЙ НА СУЩЕСТВОВАНИЕ:
"""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER,
    description TEXT,
    quantity INTEGER
    );
"""

# У нас по бизнес-требованиям получается, что каждый продукт в базе должен быть уникальным по своему id,
# поэтому можно и нужно ввести ограничение по полю product_id.

"""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY, -- теперь у нас product_id будет уникальным идентификатором
    description TEXT,
    quantity INTEGER
    );
"""

# ТАБЛИЦУ МОЖНО ОЧЕНЬ ПРОСТО УДАЛИТЬ (трудно найти, легко потерять и невозможно забыть):
"""
DROP TABLE IF EXISTS products
"""

# ВЫБОРКА ДАННЫХ ИЗ ТАБЛИЦЫ:
"""
SELECT * FROM products; -- все колонки, вся таблица
"""

# ВСТАВКА ДАННЫХ В ТАБЛИЦУ:
"""
INSERT INTO products VALUES (123, 'Лук', 120); -- вставка по всем колонкам

INSERT INTO products (product_id) VALUES (1); -- вставка в конкретное поле
"""
# Мы можем управлять обязательность полей в базе при создании таблицы:
"""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL, -- теперь при вставке данных эта колонка не может оставаться NULL
    quantity INTEGER NOT NULL -- теперь при вставке данных эта колонка не может оставаться NULL
    );
"""

# Сначала идут выборка из таблицы, потом идет сортировка выборки, затем идёт ограничение выдачи (лимит)
"""
SELECT product_id FROM products ORDER BY product_id DESC LIMIT 1;
"""

# Теперь при попытке записать данные, в которых мы что-то недодали будет падать ошибка
# А теперь давайте представим, что мы хотим, чтобы у нас id присваивался базой автоматически и
# возвращался нам в качестве ответа:

"""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL, -- теперь при вставке данных эта колонка не может оставаться NULL
    quantity INTEGER NOT NULL -- теперь при вставке данных эта колонка не может оставаться NULL
    );
"""

# # Теперь id явно вставлять не нужно:
"""
INSERT INTO products (description, quantity) VALUES ('Лук', 120) RETURNING product_id;
"""

# Теперь про отношения - можно связыавть таблицы через FOREIGN KEY - по сути наши таблицы связываются друг с другом
# через какую-либо колонку.

"""
CREATE TABLE IF NOT EXISTS shops (
    shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    address TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id) -- указываем какие колонки будут связанными
    );
"""

# Теперь у нас не получится вставить в таблицу, которая учитывает наличие продуктов в магазинах те продукты, которые
# отсутствут в базе products


"""
CREATE TABLE IF NOT EXISTS shops (
    shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    address TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
    ON UPDATE SET NULL  -- при изменении данных в соответствующей колонке в родительской таблице значение станет NULL
    ON DELETE CASCADE -- при удалении данных из родительской таблице данные в дочерней тоже будут удалены
    );
"""

# Случаются ситуации, когда нужно изменить структуру существующей таблицы, например добавить новую колонку.
# Для этого используется механизм ALTER TABLE
"""
ALTER TABLE shops ADD COLUMN created_dt TEXT;
"""

# можно организовывать лимит на выдачу строк из базы
"""
SELECT * FROM products LIMIT 2
"""

# а ещё сортировку по определённому полю
"""
SELECT * FROM products ORDER BY created_dt
"""

# Индексы - механизм, позволяющий оптимизировать поиск по таблице. Напоминает ситуацию с телефонной книгой.
# Как правило для primary key индекс во многих базах данных создаётся автоматически
"""
CREATE index description_idx ON products(quantity)
"""

# SQLite весьма легковесная БД. Для новичков это самое оно, однако надо готовиться к тому, что нужно будет переходить
# на более профессиональные типы. SQLite безоговорочно побеждает в том случае, если у вас маленький ламповый проект
# в котором нет необходимости хранить очень большие объемы данных, и где к базе производится мало запросов. А ещё она
# оооочень надёжная.

# В открытом доступе находится замечательная серверная БД PostgreSQL. Она очень мощная, распространяется бесплатно,
# а её поддержкой занимается очень большое комьюнити по всему миру.

# Для того, чтобы удобно подключаться к базам и просматривать данные можно использовать DBeaver

# в PostgreSQL будет несколько отличий в рамках того, как мы объявляем таблицу
"""
CREATE TABLE IF NOT EXISTS shops (
    shop_id SERIAL PRIMARY KEY, -- тут уже нет автоинкремента, тут serial
    description TEXT NOT NULL,
    address TEXT NOT NULL,
    created_dt date, -- появляется новый тип колонки, не строка, а дата
    product_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
    ON UPDATE SET NULL
    ON DELETE CASCADE
    );
"""

# Можно изменять существующие данные в базе:
"""UPDATE shops SET description = 'магазин неСветлый' WHERE shop_id = 3"""

# upsert - операция на вставку или обновление. То есть вставить, если такой записи нет или же обновить существующую:
"""INSERT INTO shops (shop_id, description, address,created_dt,product_id) VALUES
(5, 'магазин Темный','г.Кызыл, ул.К.Маркса, д.4','2021-05-13',87)
ON CONFLICT (shop_id) DO 
UPDATE SET description = 'магазин неТемный', address = 'г.Кызыл, ул.К.Маркса, д.4', created_dt = '2021-05-13'"""

# Модуль Datetime. Теперь немного поработаем с датами и временем.
# Годная статья - shorturl.at/awGIL (сделал шорт урл, чтобы не было длинной ссылки)
from datetime import time, date, datetime, timedelta  # time - хранит время, date - дату, datetime - и то и другое
from time import sleep

# now_datetime = datetime.now()  # получаем текущее время и дату
# print(type(now_datetime), now_datetime)

# now_date = date.today()
# print(type(now_date), now_date)

now = datetime.now()
# now_time = datetime.now().time()
# print(type(now_time), now_time)

# sleep(1)
# print(datetime.now() - now)

# строкой можно задавать шаблон отображения
# current_time = now.strftime("%H:%M:%S")
# current_time_2 = now.strftime("%d %h %Y Я ЛЮБЛЮ ПИТОН!!! %H:%M:%S")  # преобразовываем дату в строку
# print("Current Time or Date =", current_time_2, type(current_time_2))
# print(type(current_time_2), current_time_2)


# если хотим задавать часовой пояс
import pytz

# tz_NY = pytz.timezone('America/New_York')
# datetime_NY = datetime.now(tz_NY)
# print("NY time:", datetime_NY.strftime("%H:%M:%S"))

# tz_London = pytz.timezone('Europe/London')
# datetime_London = datetime.now(tz_London)
# print("London time:", datetime_London.strftime("%H:%M:%S"))

# несколько дней назад:
# my_date = datetime.now() - timedelta(days=2)
# print(my_date)

# date_time_str = '2018-06-29 08:15:27.243860'
# date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
# print(type(date_time_obj), date_time_obj)
# datestring = '2021-05-26, Я ЛЮБЛЮ ПИТОН!!! 13:05'
# date_time_obj_2 = datetime.strptime(datestring, '%Y-%m-%d, Я ЛЮБЛЮ ПИТОН!!! %H:%M')
# print(type(date_time_obj_2), date_time_obj_2)
