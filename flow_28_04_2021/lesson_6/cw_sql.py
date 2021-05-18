"""
SQL 2 ЧАСТЬ

Продолжаем работу с таблицами из домашнего задания №5:

1. Написать запрос, который должен возвращать не более 10 заявок в активном статусе, которые были созданы либо изменены
за последние 2 дня, а также ФИО и должность того, кто является создателем этой заявки.
2. Написать функцию, которая будет принимать на вход число N и с помощью запроса из п.1 будет возвращать не более N
заявок.
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
