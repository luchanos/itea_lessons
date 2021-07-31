# https://habr.com/ru/company/domclick/blog/560300/

# итераторы-генераторы
def func():
    print("Что-то выдаю в консоль")

# res = func()
# print(res)


# def skatert():
#     yield "первое блюдо", "второе", "третье"


# print(skatert)
# gen_o = skatert()
# print(next(gen_o))

def dyadechka():
    print("до 1")
    yield "Первая пуля"
    print("между 1 и 2")
    yield "Вторая пуля"
    print("между 2 и 3")
    yield "Третья пуля"
    print("между 3 и 4")
    yield "Четвертая пуля"
    print("между 4 и 5")
    yield "Пятая пуля"
    print("патроны кончились")



my_oboyma = dyadechka()  # попросил дать мне обойму
marian_ob = dyadechka()
# print(my_oboyma)

# print(next(my_oboyma))  # я осуществляю выстрел!
# print("Коля пошел поесть")
# print(next(my_oboyma))  # я осуществляю выстрел!
# print("Коля пошел покурить")
# print(next(marian_ob))
# print(next(my_oboyma))  # я осуществляю выстрел!
# print("Коля пошел в магазин")
# print(next(marian_ob))
# print(next(my_oboyma))  # я осуществляю выстрел!
# print("Коля пошел поговорить по телефону")
# print(next(my_oboyma))  # я осуществляю выстрел!
# print("Коля стрельбу завершил")
# print(next(my_oboyma))  # я осуществляю выстрел!



import sys
from time import time

# start = time()
# num = 0
# res_list = []
# while num < 100:
#     res_list.append(num)
#     num += 1

# print(time() - start)
# print(sys.getsizeof(res_list))


def simple_gen(n):
    num = 0
    while num < n:
        yield num
        num += 1


def consumer_1(n):
    v = 10
    print("1 - Процешшу принятые значения")
    cnt = 0
    while cnt < v:
        print(f"Выполняю какую-то логику со значением {next(n)}")
        cnt += 1


def consumer_2(n):
    v = 10
    print("2 - Процешшу принятые значения")
    cnt = 0
    while cnt < v:
        print(f"Выполняю какую-то логику со значением {next(n)}")
        cnt += 1


def consumer_3(n):
    v = 10
    print("3 - Процешшу принятые значения")
    cnt = 0
    while cnt < v:
        print(f"Выполняю какую-то логику со значением {next(n)}")
        cnt += 1


# gen_o = simple_gen(100)
# cnt = 0
# consumer_1(gen_o)
# consumer_2(gen_o)
# consumer_3(gen_o)
#
# print(time() - start)
# print(sys.getsizeof(gen_o))

# gen_o = simple_gen(10)
# print(1 in gen_o)
# print(1 in gen_o)

l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# for el in l:
#     print(el)

it_obj = iter(l)
print(it_obj)
try:
    while True:
        print(next(it_obj))
except StopIteration:
    pass
