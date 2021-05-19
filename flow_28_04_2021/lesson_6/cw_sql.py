"""
SQL 2 ЧАСТЬ

Продолжаем работу с таблицами из домашнего задания №5:

1. Создать тестовый набор данных по каждой из таблиц в модуле python (лучше всего использовать список списков или
список кортежей). Написать скрипт, который бы осуществлял подключение к существующей БД и последовательно запускал
сначала скрипты на создание таблиц (из прошлого ДЗ: departments, employees, orders), а затем последовательно загружал
туда данные.

2. По тестовым данным необходимо написать следующие запросы:
    - запрос для получения заявок в определённом статусе (можно выбрать любой) за конкретный день, созданных
    конкретным сотрудником;
    - запрос, возвращающий список сотрудников и департаментов, в которых они работают
    - запрос, позволяющий получить количество заявок в определенном статусе (можно выбрать любой) по дням;
"""

# JOINs
# https://www.postgresqltutorial.com/postgresql-joins/
# https://habr.com/ru/post/448072/

# cross join - все возмоные комбинации строк из скрещиваемых наборов
"""
SELECT * FROM shops CROSS JOIN products;
"""

# inner join - все комбинации соединений строк с неким фильтром condition
"""
SELECT * FROM shops INNER JOIN products ON shops.product_id = products.product_id
"""

# оно будет аналогично

"""
SELECT * FROM shops CROSS JOIN products WHERE shops.product_id = products.product_id
"""

# left join - то же самое, что inner join (все комбинации соединений строк, отфильтрованных по какому-то условию) +
# добавляются записи из левой таблицы, для которых в правой таблице по фильтру ничего не попало

"""
SELECT * FROM shops LEFT JOIN products ON shops.product_id = products.product_id
"""

# можно прекрасно использовать математические функции, применительно к колонкам таблицы - такие функции
# называются агрегатными
"""
SELECT sum(quantity) FROM products;
SELECT avg(quantity) FROM products;
SELECT max(quantity) FROM products;
SELECT min(quantity) FROM products;
"""

# а ещё в sql можно группировать значения по колонкам
"""
SELECT count(*), description FROM products GROUP BY (description)
"""
