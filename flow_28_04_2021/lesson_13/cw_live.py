"""
Сделать шаблоны для отображения сотрудников, заявок и департаментов и прикрутить их к соответствующим flask-методам.
Используйте 1 базовый шаблон, от которого унаследуйте все остальные. Что хотелось бы видеть:
 - навигационную панель (можно взять из классной работы или написать свою собственную)
 - удобный вывод информации (ограничение по количеству записей, выводимых на экран и использование
 списка с точками или цифрами при выводе)
"""

from time import sleep

# Пул потоков
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randrange

b = 0

# def f(a):
#     global b
#     print("This is %d" % b)
#     b += 1
#     # sleep_time = randrange(0, 10)
#     # time.sleep(sleep_time)
#     sleep(1)
#     buf = b
#     return f"result {a * a} for thread {buf}"

# шаг 1 - создаём пул потоков с количество воркеров, которое будет равно количеству создаваемых потоков на исполнение
# под капотом
# шаг 2 - с помощью функции .submit у объекта ThreadPoolExecutor приговариваем наши задачи к исполнению.
# шаг 3 - с помошью as_completed и метода .result() у объекта future получаем долгожданный результат.
# with ThreadPoolExecutor(max_workers=10) as pool:  # тут всё само сделается!
#     results = [pool.submit(f, i) for i in range(10)]  # submit - создает футуру, это объект, который обещает исполнится
#     for future in as_completed(results):
#         print(future.result())
